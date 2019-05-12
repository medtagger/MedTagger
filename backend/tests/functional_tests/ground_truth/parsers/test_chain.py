"""Tests for Chain Parser."""
from typing import Any

import numpy as np

from medtagger.database import models
from medtagger.types import Point
from medtagger.ground_truth.parsers import chain
from medtagger.repositories import (
    labels as LabelsRepository,
    users as UsersRepository,
)

from tests.functional_tests import helpers

SLICE_HEIGHT = 512
SLICE_WIDTH = 512


def test_parsing_chain_label_elements(prepare_environment: Any) -> None:
    """Test parsing Chain Label Element to numpy array."""
    user_id = UsersRepository.add_new_user(models.User('user@medtagger', 'HASH', 'Admin', 'Admin'))
    user = UsersRepository.get_user_by_id(user_id)
    scan, label_tag = helpers.prepare_scan_and_tag_for_labeling()
    label = helpers.prepare_empty_label(scan, user)
    for slice_index in range(3):
        points = [
            Point(x=0, y=0),
            Point(x=1, y=0),
            Point(x=1, y=1),
            Point(x=0, y=1),
        ]
        LabelsRepository.add_new_chain_label_element(label.id, slice_index, label_tag, points, loop=True)

    query = models.ChainLabelElement.query.join(models.Label)
    query = query.filter(models.Label.scan_id == scan.id)
    label_elements = query.all()

    parser = chain.ChainLabelElementParser()
    data = parser.convert_to_numpy(label_elements)
    assert data.shape == (3, SLICE_WIDTH * SLICE_HEIGHT)
    assert data.sum() == 3 * SLICE_WIDTH * SLICE_HEIGHT  # Squares fill whole Slice


def test_chain_intersection_over_union(prepare_environment: Any) -> None:
    """Test computing IoU measure for Chain Label Elements."""
    parser = chain.ChainLabelElementParser()

    # Zero overlapping
    iou = parser.compute_intersection_over_union(np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 0]),
                                                 np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1]))
    assert iou == 0.0

    # A little bit of an overlap
    iou = parser.compute_intersection_over_union(np.array([1, 1, 1, 1, 1, 1, 1, 0, 0, 0]),
                                                 np.array([0, 0, 0, 1, 1, 1, 1, 1, 1, 1]))
    assert iou == 0.4

    # Both chains fill whole Slice
    iou = parser.compute_intersection_over_union(np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
                                                 np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]))
    assert iou == 1.0
