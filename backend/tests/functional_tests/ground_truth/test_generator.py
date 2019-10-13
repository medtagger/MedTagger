"""Tests for Ground Truth data set generator."""
import math
from typing import Any

import numpy as np

from medtagger.database import models
from medtagger.types import LabelPosition, LabelShape
from medtagger.ground_truth import generator
from medtagger.ground_truth.algorithms import majority_voting
from medtagger.repositories import (
    labels as LabelsRepository,
    users as UsersRepository,
)

from tests.functional_tests import helpers


def test_data_set_generator(prepare_environment: Any) -> None:  # pylint: disable=too-many-locals
    """Test Data Set Generator against rectangular Label Elements from real database."""
    user_id = UsersRepository.add_new_user(models.User('user@medtagger', 'HASH', 'Admin', 'Admin'))
    user = UsersRepository.get_user_by_id(user_id)
    scan, label_tag = helpers.prepare_scan_and_tag_for_labeling()

    label_a = helpers.prepare_empty_label(scan, user)
    for slice_index in range(3):
        LabelsRepository.add_new_rectangular_label_element(label_a.id, LabelPosition(x=1, y=1, slice_index=slice_index),
                                                           LabelShape(width=0, height=0), label_tag)
    label_b = helpers.prepare_empty_label(scan, user)
    for slice_index in range(3):
        LabelsRepository.add_new_rectangular_label_element(label_b.id, LabelPosition(x=0, y=0, slice_index=slice_index),
                                                           LabelShape(width=1, height=1), label_tag)
    label_c = helpers.prepare_empty_label(scan, user)
    for slice_index in range(3):
        LabelsRepository.add_new_rectangular_label_element(label_c.id, LabelPosition(x=1, y=1, slice_index=slice_index),
                                                           LabelShape(width=0, height=0), label_tag)

    algorithm = majority_voting.MajorityVotingAlgorithm()
    data_set_generator = generator.DataSetGenerator(algorithm)

    query = models.RectangularLabelElement.query.join(models.Label)
    query = query.filter(models.Label.scan_id == scan.id)
    label_elements = query.all()

    ground_truth_for_slice_id = data_set_generator.generate(label_elements)
    assert sorted(list(ground_truth_for_slice_id.keys())) == sorted([_slice.id for _slice in scan.slices])

    example_slice_id = scan.slices[0].id
    expected_ground_truth = np.array([1, 1, 1, 1])
    assert ground_truth_for_slice_id[example_slice_id].shape == expected_ground_truth.shape

    ground_truth = ground_truth_for_slice_id[example_slice_id]
    for i in range(expected_ground_truth.shape[0]):  # pylint: disable=unsubscriptable-object  # Astroid>2.3 bug
        assert math.isclose(ground_truth[i], expected_ground_truth[i], abs_tol=1e-5)
