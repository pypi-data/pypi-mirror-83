#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2020 CoML

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# Rachid RIAD & Hadrien TITEUX
"""
##########
Continuum and corpus
##########

"""
import csv
import logging
import random
from functools import lru_cache
from pathlib import Path
from typing import Optional, Dict, Tuple, List, Union, Set, Iterable, TYPE_CHECKING

import cvxpy as cp
import numpy as np
from dataclasses import dataclass
from pyannote.core import Annotation, Segment, Timeline
from pyannote.database.util import load_rttm
from sortedcontainers import SortedDict
from typing_extensions import Literal

from .dissimilarity import AbstractDissimilarity
from .numba_utils import chunked_cartesian_product

if TYPE_CHECKING:
    from .alignment import UnitaryAlignment, Alignment

CHUNK_SIZE = 2 ** 25

# defining Annotator type
Annotator = str
PivotType = Literal["float_pivot", "int_pivot"]

# percentages for the precision
PRECISION_LEVEL = {
    "high": 0.01,
    "medium": 0.02,
    "low": 0.1
}


@dataclass
class Unit:
    segment: Segment
    annotation: Optional[str] = None


class Continuum:
    """Continuum

    Parameters
    ----------
    uri : string, optional
        name of annotated resource (e.g. audio or video file)
    modality : string, optional
        name of annotated modality
    """

    @classmethod
    def from_csv(cls,
                 path: Union[str, Path],
                 discard_invalid_rows=True,
                 delimiter: str = ","):
        """
        Load annotations from a CSV file , with structure
        annotator, category, segment_start, segment_end

        Parameters
        ----------
        path: path or str
            Path to the CSV file storing annotations
        discard_invalid_rows: bool
            Path: if a row contains invalid annotations, discard it)
        delimiter: str, default ","
            CSV delimiter

        Returns
        -------
        A new continuum object

        """
        if isinstance(path, str):
            path = Path(path)

        continuum = cls()
        with open(path) as csv_file:
            reader = csv.reader(csv_file, delimiter=delimiter)
            for row in reader:
                seg = Segment(float(row[2]), float(row[3]))
                try:
                    continuum.add(row[0], seg, row[1])
                except ValueError as e:
                    if discard_invalid_rows:
                        print(f"Discarded invalid segment : {str(e)}")
                    else:
                        raise e

        return continuum

    @classmethod
    def from_rttm(cls, path: Union[str, Path]) -> 'Continuum':
        """
        Load annotations from a RTTM file. The file name field will be used
        as an annotation's annotator

        Parameters
        ----------
        path: path or str
            Path to the CSV file storing annotations

        Returns
        -------
        A new continuum object
        """
        annotations = load_rttm(str(path))
        continuum = cls()
        for uri, annot in annotations.items():
            continuum.add_annotation(uri, annot)
        return continuum

    @classmethod
    def sample_from_continuum(cls, continuum: 'Continuum',
                              pivot_type: PivotType = "float_pivot",
                              ground_truth_annotators: Optional[List[Annotator]] = None) -> 'Continuum':
        assert pivot_type in ('float_pivot', 'int_pivot')
        """Generate a new random annotation from a single continuum
                Strategy from figure 12

                >>> gamma_agreement.sample_from_single_continuum()
                ... <pyannote.core.annotation.Annotation at 0x7f5527a19588>
                """
        last_start_time = max(unit.segment.start for unit in continuum.iterunits())
        new_continuum = Continuum()
        if ground_truth_annotators is not None:
            assert set(continuum.annotators).issuperset(set(ground_truth_annotators))
            annotators = ground_truth_annotators
        else:
            annotators = continuum.annotators

        # TODO: why not sample from the whole continuum?
        # TODO : shouldn't the sampled annotators nb be equal to the annotators amount?
        for idx in range(continuum.num_annotators):
            if pivot_type == 'float_pivot':
                pivot = random.uniform(continuum.avg_length_unit, last_start_time)
            else:
                pivot = random.randint(np.floor(continuum.avg_length_unit),
                                       np.ceil(last_start_time))

            rnd_annotator = random.choice(annotators)
            units = continuum._annotations[rnd_annotator]
            sampled_annotation = SortedDict()
            for segment, unit in units.items():
                if pivot < segment.start:
                    new_segment = Segment(segment.start - pivot, segment.end - pivot)
                else:
                    new_segment = Segment(segment.start + pivot, segment.end + pivot)
                sampled_annotation[new_segment] = Unit(new_segment, unit.annotation)
            new_continuum._annotations[f'Sampled_annotation {idx}'] = sampled_annotation
        return new_continuum

    def __init__(self, uri: Optional[str] = None):
        self.uri = uri
        # Structure {annotator -> { segment -> unit}}
        self._annotations = SortedDict()

        # these are instanciated when compute_disorder is called
        self._chosen_alignments: np.ndarray = None
        self._alignments_disorders: np.ndarray = None

    def __bool__(self):
        """Truthiness, basically tests for emptiness

        >>> if continuum:
        ...    # continuum is not empty
        ... else:
        ...    # continuum is empty
        """
        return len(self._annotations) > 0

    def __len__(self):
        return len(self._annotations)

    @property
    def num_units(self) -> int:
        """Number of units"""
        return sum(len(units) for units in self._annotations.values())

    @property
    def categories(self) -> Set[str]:
        return set(unit.annotation for unit in self.iterunits()
                   if unit.annotation is not None)

    @property
    def num_annotators(self) -> int:
        """Number of annotators"""
        return len(self._annotations)

    @property
    def avg_num_annotations_per_annotator(self):
        """Average number of annotated segments per annotator"""
        return self.num_units / self.num_annotators

    @property
    def max_num_annotations_per_annotator(self):
        """The maximum number of annotated segments an annotator has
        in this continuum"""
        max_num_annotations_per_annotator = 0
        for annotator in self._annotations:
            max_num_annotations_per_annotator = np.max(
                [max_num_annotations_per_annotator,
                 len(self[annotator])])
        return max_num_annotations_per_annotator

    @property
    def avg_length_unit(self):
        """Mean of the annotated segments' durations"""
        return sum(unit.segment.duration for unit in self.iterunits()) / self.num_units

    def add(self, annotator: Annotator, segment: Segment, annotation: Optional[str] = None):
        """
        Add a segment to the continuum

        Parameters
        ----------
        annotator: str
            The annotator that produced the added annotation
        segment: `pyannote.core.Segment`
            The segment for that annotation
        annotation: optional str
            That segment's annotation, if any.
        """
        if segment.duration == 0.0:
            raise ValueError("Tried adding segment of duration 0.0")

        if annotator not in self._annotations:
            self._annotations[annotator] = SortedDict()

        self._annotations[annotator][segment] = Unit(segment, annotation)

        # units array has to be updated, nullifying
        if self._alignments_disorders is not None:
            self._chosen_alignments = None
            self._alignments_disorders = None

    def add_annotation(self, annotator: Annotator, annotation: Annotation):
        for label in annotation.labels():
            for segment in annotation.label_timeline(label):
                self.add(annotator, segment, label)

    def add_timeline(self, annotator: Annotator, timeline: Timeline):
        for segment in timeline:
            self.add(annotator, segment)

    def from_textgrid(self,
                      annotator: Annotator,
                      tg_path: Union[str, Path],
                      selected_tiers: Optional[List[str]] = None):
        from textgrid import TextGrid, IntervalTier
        tg = TextGrid.fromFile(str(tg_path))
        for tier_name in tg.getNames():
            if selected_tiers is not None and tier_name not in selected_tiers:
                continue
            tier: IntervalTier = tg.getFirst(tier_name)
            for interval in tier:
                self.add(annotator,
                         Segment(interval.minTime, interval.maxTime),
                         interval.mark)

    def __getitem__(self, *keys: Union[Annotator, Tuple[Annotator, Segment]]) \
            -> Union[SortedDict, Unit]:
        """Get annotation object

        >>> annotation = continuum[annotator]
        """
        if len(keys) == 1:
            annotator = keys[0]
            return self._annotations[annotator]
        elif len(keys) == 2 and isinstance(keys[2], Segment):
            annotator, segment = keys
            return self._annotations[annotator][segment]

    def __iter__(self) -> Iterable[Tuple[Annotator, SortedDict]]:
        return iter(self._annotations.items())

    @property
    def annotators(self):
        """List all annotators in the Continuum
        # TODO: doc example
        """
        return list(self._annotations.keys())

    def iterunits(self):
        """Iterate over units (in chronological order)

        >>> for annotator in annotation.iterannotators():
        ...     # do something with the annotator
        """
        for units in self._annotations.values():
            yield from units.values()

    def compute_disorders(self, dissimilarity: AbstractDissimilarity):
        assert isinstance(dissimilarity, AbstractDissimilarity)
        assert len(self.annotators) >= 2

        disorder_args = dissimilarity.build_args(self)

        nb_unit_per_annot = [len(arr) + 1 for arr in self._annotations.values()]
        all_disorders = []
        all_valid_tuples = []
        for tuples_batch in chunked_cartesian_product(nb_unit_per_annot, CHUNK_SIZE):
            batch_disorders = dissimilarity(tuples_batch, *disorder_args)

            # Property section 5.1.1 to reduce initial complexity
            valid_disorders_ids, = np.where(batch_disorders < self.num_annotators * dissimilarity.delta_empty)
            all_disorders.append(batch_disorders[valid_disorders_ids])
            all_valid_tuples.append(tuples_batch[valid_disorders_ids])

        disorders = np.concatenate(all_disorders)
        possible_unitary_alignments = np.concatenate(all_valid_tuples)

        # Definition of the integer linear program
        num_possible_unitary_alignements = len(disorders)
        x = cp.Variable(shape=num_possible_unitary_alignements, boolean=True)

        true_units_ids = []
        num_units = 0
        for units in self._annotations.values():
            true_units_ids.append(np.arange(num_units, num_units + len(units)).astype(np.int32))
            num_units += len(units)

        # Constraints matrix
        A = np.zeros((num_units, num_possible_unitary_alignements))

        for p_id, unit_ids_tuple in enumerate(possible_unitary_alignments):
            for annotator_id, unit_id in enumerate(unit_ids_tuple):
                if unit_id != len(true_units_ids[annotator_id]):
                    A[true_units_ids[annotator_id][unit_id], p_id] = 1

        obj = cp.Minimize(disorders.T @ x)
        constraints = [cp.matmul(A, x) == 1]
        prob = cp.Problem(obj, constraints)

        # we don't actually care about the optimal loss value
        optimal_value = prob.solve()

        # compare with 0.9 as cvxpy returns 1.000 or small values i.e. 10e-14
        chosen_alignments_ids, = np.where(x.value > 0.9)
        self._chosen_alignments = possible_unitary_alignments[chosen_alignments_ids]
        self._alignments_disorders = disorders[chosen_alignments_ids]
        return self._alignments_disorders.sum() / len(self._alignments_disorders)

    def get_best_alignment(self, dissimilarity: Optional['AbstractDissimilarity'] = None):
        if self._chosen_alignments is None or self._alignments_disorders is None:
            if dissimilarity is not None:
                self.compute_disorders(dissimilarity)
            else:
                raise ValueError("Best alignment disorder hasn't been computed, "
                                 "a the dissimilarity argument is required")

        from .alignment import UnitaryAlignment, Alignment

        set_unitary_alignements = []
        for alignment_id, alignment in enumerate(self._chosen_alignments):
            u_align_tuple = []
            for annotator_id, unit_id in enumerate(alignment):
                annotator, units = self._annotations.peekitem(annotator_id)
                try:
                    _, unit = units.peekitem(unit_id)
                    u_align_tuple.append((annotator, unit))
                except IndexError:  # it's a "null unit"
                    u_align_tuple.append((annotator, None))
            unitary_alignment = UnitaryAlignment(tuple(u_align_tuple))
            unitary_alignment.disorder = self._alignments_disorders[alignment_id]
            set_unitary_alignements.append(unitary_alignment)
        return Alignment(set_unitary_alignements, continuum=self, check_validity=True)

    def compute_gamma(self,
                      dissimilarity: 'AbstractDissimilarity',
                      n_samples: int = 30,
                      # TODO: figure out if this should be optional or not
                      precision_level: Optional[float] = None,
                      ground_truth_annotators: Optional[List[Annotator]] = None,
                      sampling_strategy: str = "single",
                      pivot_type: PivotType = "float_pivot",
                      random_seed: Optional[float] = 4577
                      ) -> 'GammaResults':
        """

        Parameters
        ----------
        dissimilarity: AbstractDissimilarity
            dissimilarity instance. Used to compute the disorder between units.
        n_samples: optional int
            number of random continuum sampled from this continuum  used to
            estimate the gamma measure
        precision_level: optional float
            error percentage of the gamma estimation.
        ground_truth_annotators:
            if set, the random continuua will only be sampled from these
            annotators. This should be used when you want to compare a prediction
            against some ground truth annotation.
        pivot_type: 'float_pivot' or 'int_pivot'
            pivot type to be used when sampling continuua
        random_seed: optional float, int or str
            random seed used to set up the random state before sampling the
            random continuua

        Returns
        -------

        """
        assert sampling_strategy in ("single", "multi")
        if sampling_strategy == "multi":
            raise NotImplemented("Multi-continuum sampling strategy is not "
                                 "supported for now")

        if random_seed is not None:
            random.seed(random_seed)

        chance_disorders = []
        for _ in range(n_samples):
            sampled_continuum = Continuum.sample_from_continuum(self, pivot_type, ground_truth_annotators)
            sample_disorder = sampled_continuum.compute_disorders(dissimilarity)
            chance_disorders.append(sample_disorder)

        if precision_level is not None:
            assert 0 < precision_level < 1.0
            # taken from subsection 5.3 of the original paper
            # confidence at 95%, eg, 1.96
            variation_coeff = np.std(chance_disorders) / np.mean(chance_disorders)
            confidence = 1.96
            required_samples = np.ceil((variation_coeff * confidence / precision_level) ** 2).astype(np.int32)
            logging.debug(f"Number of required samples for confidence {precision_level}: {required_samples}")
            if required_samples > n_samples:
                for _ in range(required_samples - n_samples):
                    sampled_continuum = Continuum.sample_from_continuum(self, pivot_type, ground_truth_annotators)
                    sample_disorder = sampled_continuum.compute_disorders(dissimilarity)
                    chance_disorders.append(sample_disorder)
        best_alignment = self.get_best_alignment(dissimilarity)

        return GammaResults(
            best_alignment=best_alignment,
            pivot_type=pivot_type,
            n_samples=n_samples,
            chance_disorders=np.array(chance_disorders),
            precision_level=precision_level
        )

    def compute_gamma_cat(self):
        raise NotImplemented()

    def to_csv(self, path: Union[str, Path], delimiter=","):
        if isinstance(path, str):
            path = Path(path)
        with open(path, "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=delimiter)
            for annotator, units in self._annotations.items():
                for unit in units.values():
                    writer.writerow([annotator, unit.annotation, unit.segment.start, unit.segment.end])


@dataclass
class GammaResults:
    """
    Gamma results object. Stores information about a gamma measure computation.
    """
    best_alignment: 'Alignment'
    pivot_type: PivotType
    n_samples: int
    chance_disorders: np.ndarray
    precision_level: Optional[float] = None

    @property
    def alignments_nb(self):
        return len(self.best_alignment.unitary_alignments)

    @property
    def observed_agreement(self) -> float:
        """Returns the disorder of the computed best alignment, i.e, the
        observed agreement."""
        return self.best_alignment.disorder

    @property
    def expected_disagreement(self) -> float:
        """Returns the expected disagreement for computed random samples, i.e.,
        the mean of the sampled continuua's disorders"""
        return self.chance_disorders.mean()

    @property
    def expected_gamma_boundaries(self):
        """Returns a tuple of the expected boundaries of the computed gamma,
         obtained using the expected disagreement and the precision level"""
        if self.precision_level is None:
            raise ValueError("No precision level has been set, cannot compute"
                             "the gamma boundaries")
        return (1 - self.observed_agreement / (self.expected_disagreement *
                                               (1 - self.precision_level)),
                1 - self.observed_agreement / (self.expected_disagreement *
                                               (1 + self.precision_level)))

    @property
    def gamma(self):
        """Returns the gamma value"""
        return 1 - self.observed_agreement / self.expected_disagreement
