"""Tests for K-Means algorithm."""
import math
from typing import Any

import numpy as np

from medtagger.ground_truth.algorithms import k_means


def test_k_means_algorithm(prepare_environment: Any) -> None:
    """Test for a simple case resolved using K-Means algorithm."""
    data = np.array([
        [0, 0, 1, 1],
        [0, 0, 1, 1],
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 1, 0, 0],
    ])
    algorithm = k_means.KMeansAlgorithm()
    ground_truth = algorithm.get_ground_truth(data)
    expected_ground_truth = np.array([1, 1, 0, 0])
    assert ground_truth.shape == expected_ground_truth.shape
    for i in range(expected_ground_truth.shape[0]):  # pylint: disable=unsubscriptable-object  # Astroid>2.3 bug
        assert math.isclose(ground_truth[i], expected_ground_truth[i], abs_tol=1e-5)
