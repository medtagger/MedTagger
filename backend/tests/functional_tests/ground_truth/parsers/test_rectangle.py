"""Tests for Rectangle Parser."""
import math
from typing import Any

import numpy as np

from medtagger.database import models
from medtagger.types import LabelPosition, LabelShape
from medtagger.ground_truth.parsers import rectangle
from medtagger.repositories import (
    labels as LabelsRepository,
    users as UsersRepository,
)

from tests.functional_tests import helpers

SLICE_HEIGHT = 512
SLICE_WIDTH = 512


def test_parsing_rectangle_label_elements(prepare_environment: Any) -> None:
    """Test parsing Rectangle Label Element to numpy array."""
    user_id = UsersRepository.add_new_user(models.User('user@medtagger', 'HASH', 'Admin', 'Admin'))
    user = UsersRepository.get_user_by_id(user_id)
    scan, label_tag = helpers.prepare_scan_and_tag_for_labeling()
    label = helpers.prepare_empty_label(scan, user)
    for slice_index in range(3):
        LabelsRepository.add_new_rectangular_label_element(label.id, LabelPosition(x=1, y=1, slice_index=slice_index),
                                                           LabelShape(width=0, height=0), label_tag)

    query = models.RectangularLabelElement.query.join(models.Label)
    query = query.filter(models.Label.scan_id == scan.id)
    label_elements = query.all()

    parser = rectangle.RectangleLabelElementParser()
    data = parser.convert_to_numpy(label_elements)
    assert data.shape == (3, 4)

    expected_data = (1, 1, 1, 1)
    for i in range(4):
        assert math.isclose(data[0][i], expected_data[i], abs_tol=1e-5)


def test_rectangle_intersection_over_union(prepare_environment: Any) -> None:
    """Test computing IoU measure for Rectangle Label Elements."""
    parser = rectangle.RectangleLabelElementParser()

    # Zero overlapping
    iou = parser.compute_intersection_over_union(np.array([1, 1, 1, 1]),
                                                 np.array([0, 0, 0, 0]))
    assert iou == 0.0

    # A little bit of an overlap
    iou = parser.compute_intersection_over_union(np.array([0, 0, 0.5, 0.5]),
                                                 np.array([0, 0, 0.5, 1.0]))
    assert iou == 0.5

    # Both rectangles are the same
    iou = parser.compute_intersection_over_union(np.array([0.25, 0.25, 0.75, 0.75]),
                                                 np.array([0.25, 0.25, 0.75, 0.75]))
    assert iou == 1.0
