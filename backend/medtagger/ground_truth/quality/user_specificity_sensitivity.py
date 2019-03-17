"""Implementation of a Specificity and Sensitivity measure calculation."""
import collections
from typing import List, Dict, Set, Tuple

import numpy as np

from medtagger.database import models
from medtagger.ground_truth import parsers
from medtagger.ground_truth.algorithms.base import GeneratorAlgorithm


INTERSECTION_OVER_UNION_THRESHOLD = 0.4


def compute_specificity_and_sensitivity_for_users(
        algorithm: GeneratorAlgorithm, users: Set[models.User], label_elements: List[models.LabelElement],
        ground_truth: Dict[str, np.ndarray]) -> Tuple[Dict[str, float], Dict[str, float], Dict[str, float]]:
    """Compute Specificity and Sensitivity measure for each User.

    Specificity = True Negative / Negative
    Sensitivity = True Positive / Positive

    :param algorithm: algorithm used during Ground Truth generation
    :param users: set of Users that took part in data set generation
    :param label_elements: list of Label Elements used for data set generation
    :param ground_truth: Ground Truth data set as mapping of SliceID to numpy representation
    :return: tuple with mappings of specificities, sensitivities and scores for each UserID
    """
    specificity = collections.defaultdict(lambda: 0)
    sensitivity = collections.defaultdict(lambda: 0)
    scores = collections.defaultdict(lambda: 0)

    labels_for_slice_id = collections.defaultdict(list)
    for label_element in label_elements:
        labeled_slice = label_element.label.scan.slices[label_element.slice_index]
        labels_for_slice_id[labeled_slice.id].append(label_element)

    slices_ids = list(ground_truth.keys())
    users_ids = [user.id for user in users]
    for user_id in users_ids:
        true_positive, true_negative = 0, 0
        positive, negative = 0, 0

        user_label_elements_ids = {e.id for e in label_elements if e.label.owner_id == user_id}

        for slice_id in slices_ids:
            label_elements_ids = {e.id for e in labels_for_slice_id[slice_id]}

            # In case there are not enough Labels for this Slice, we may assume
            # that there is nothing interesting
            if len(label_elements_ids) < 2:
                if len(user_label_elements_ids.intersection(label_elements_ids)):
                    # User labeled Slice that does not have anything - it's a fail
                    true_negative += 0
                else:
                    # User didn't label this Slice - it's fine!
                    true_negative += 1
                negative += 1
                continue  # Skipping as we won't have any Ground Truth for this Slice

            user_label_element = next((e for e in labels_for_slice_id.get(slice_id, []) if e.label.owner.id == user_id), None)
            if user_label_element is None:
                true_positive += 0  # User didn't find anything on this Slice
                positive += 1
                continue  # Doesn't make sense to do any computations, let's move on

            parser = parsers.get_parser(type(label_elements[0]))
            user_annotation = parser.convert_to_numpy([user_label_element], algorithm.REQUIRE_IMAGE_RESIZE)[0]
            ground_truth_annotation = ground_truth[slice_id]
            metric = parser.compute_intersection_over_union(user_annotation, ground_truth_annotation)

            true_positive += int(metric > INTERSECTION_OVER_UNION_THRESHOLD)
            positive += 1

        sensitivity[user_id] = true_positive / positive
        specificity[user_id] = true_negative / negative
        scores[user_id] = (sensitivity[user_id] + specificity[user_id] - 1) ** 2

    return specificity, sensitivity, scores
