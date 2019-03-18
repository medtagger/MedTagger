"""Implementation of a Specificity and Sensitivity measure calculation."""
import collections
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple

import numpy as np

from medtagger.types import SliceID, UserID
from medtagger.database import models
from medtagger.ground_truth import parsers
from medtagger.ground_truth.algorithms.base import GeneratorAlgorithm


INTERSECTION_OVER_UNION_THRESHOLD = 0.4


@dataclass
class Statistics:
    """Representation of statistics for a single User or a change (delta) to these Statistics."""

    true_positive: int = 0
    positive: int = 0
    true_negative: int = 0
    negative: int = 0


def compute_specificity_and_sensitivity_for_users(
        algorithm: GeneratorAlgorithm, users: Set[models.User], label_elements: List[models.LabelElement],
        ground_truth: Dict[SliceID, np.ndarray]) \
        -> Tuple[Dict[UserID, float], Dict[UserID, float], Dict[UserID, float]]:
    """Compute Specificity and Sensitivity measure for each User.

    Specificity = True Negative / Negative
    Sensitivity = True Positive / Positive

    IMPORTANT NOTE: For now, this method assumes that there is only one Label Element with given type for each
                    Slice in examined Scans. This will be extended in the future, once we will collect test data
                    for experiments and analysis.

    :param algorithm: algorithm used during Ground Truth generation
    :param users: set of Users that took part in data set generation
    :param label_elements: list of Label Elements used for data set generation
    :param ground_truth: Ground Truth data set as mapping of SliceID to numpy representation
    :return: tuple with mappings of specificities, sensitivities and scores for each UserID
    """  # pylint: disable=too-many-locals  # All of these local variables are needed to keep this code readable
    specificity: Dict[UserID, float] = collections.defaultdict(lambda: 0)
    sensitivity: Dict[UserID, float] = collections.defaultdict(lambda: 0)
    scores: Dict[UserID, float] = collections.defaultdict(lambda: 0)

    label_elements_for_slice_id: Dict[SliceID, List[models.LabelElement]] = collections.defaultdict(list)
    for label_element in label_elements:
        labeled_slice = label_element.label.scan.slices[label_element.slice_index]
        label_elements_for_slice_id[labeled_slice.id].append(label_element)

    slices_ids = list(ground_truth.keys())
    for user_id in {user.id for user in users}:
        user_statistics = Statistics()
        for slice_id in slices_ids:
            all_label_elements_for_this_slice = label_elements_for_slice_id[slice_id]
            user_label_elements_for_this_slice = [e for e in all_label_elements_for_this_slice
                                                  if e.label.owner.id == user_id]
            ground_truth_annotation = ground_truth[slice_id]
            delta = _analyse_user_label_elements(algorithm, user_label_elements_for_this_slice,
                                                 all_label_elements_for_this_slice, ground_truth_annotation)
            user_statistics.true_positive += delta.true_positive
            user_statistics.true_negative += delta.true_negative
            user_statistics.positive += delta.positive
            user_statistics.negative += delta.negative

        sensitivity[user_id] = user_statistics.true_positive / user_statistics.positive
        specificity[user_id] = user_statistics.true_negative / user_statistics.negative
        scores[user_id] = (sensitivity[user_id] + specificity[user_id] - 1) ** 2

    return specificity, sensitivity, scores


def _analyse_user_label_elements(algorithm: GeneratorAlgorithm,
                                 user_label_elements_for_this_slice: List[models.LabelElement],
                                 all_label_elements_for_this_slice: List[models.LabelElement],
                                 ground_truth_annotation: np.ndarray) -> Statistics:
    """Analyse all user Label Elements against Ground Truth annotation.

    :param algorithm: algorithm used for Ground Truth generation
    :param user_label_elements_for_this_slice:
    :param all_label_elements_for_this_slice:
    :param ground_truth_annotation:
    :return:
    """
    all_label_elements_ids = {e.id for e in all_label_elements_for_this_slice}
    user_label_elements_ids = {e.id for e in user_label_elements_for_this_slice}

    # In case there are not enough Labels for this Slice, we may assume that there is nothing interesting
    number_of_label_elements_on_this_slice = len(all_label_elements_ids)
    if number_of_label_elements_on_this_slice < 2:
        if user_label_elements_ids.intersection(all_label_elements_ids):
            # User labeled Slice that does not have anything - it's a fail
            return Statistics(true_negative=0, negative=1)

        # User didn't label this Slice - it's fine!
        return Statistics(true_negative=1, negative=1)

    if not user_label_elements_ids:
        # User didn't find anything on this Slice - it's a fail
        return Statistics(true_positive=0, positive=1)

    parser = parsers.get_parser(type(user_label_elements_for_this_slice[0]))
    user_annotation = parser.convert_to_numpy(user_label_elements_for_this_slice, algorithm.REQUIRE_IMAGE_RESIZE)[0]
    metric = parser.compute_intersection_over_union(user_annotation, ground_truth_annotation)

    return Statistics(true_positive=int(metric > INTERSECTION_OVER_UNION_THRESHOLD), positive=1)
