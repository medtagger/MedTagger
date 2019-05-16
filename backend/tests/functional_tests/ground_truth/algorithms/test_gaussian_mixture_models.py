"""Tests for Gaussian Mixture Models algorithm."""
import math
from typing import Any

import numpy as np

from medtagger.ground_truth.algorithms import gaussian_mixture_models


def test_gaussian_mixture_models_algorithm(prepare_environment: Any) -> None:
    """Test for a simple case resolved using Gaussian Mixture Models algorithm."""
    data = np.array([
        [0, 0, 1, 1],
        [0, 0, 1, 1],
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 1, 0, 0],
    ])
    algorithm = gaussian_mixture_models.GaussianMixtureModelsAlgorithm()
    ground_truth = algorithm.get_ground_truth(data)
    expected_ground_truth = np.array([1, 1, 0, 0])
    assert ground_truth.shape == expected_ground_truth.shape
    for i in range(expected_ground_truth.shape[0]):
        assert math.isclose(ground_truth[i], expected_ground_truth[i], abs_tol=1e-5)
