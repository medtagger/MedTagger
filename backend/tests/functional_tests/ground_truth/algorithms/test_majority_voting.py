"""Tests for Majority Voting algorithm."""
import math
from typing import Any

import numpy as np

from medtagger.ground_truth.algorithms import majority_voting


def test_majority_voting_algorithm(prepare_environment: Any) -> None:
    """Test for a simple case resolved using Majority Voting algorithm."""
    data = np.array([
        [0, 0, 1, 1],
        [0, 0, 1, 1],
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 1, 0, 0],
    ])
    algorithm = majority_voting.MajorityVotingAlgorithm()
    ground_truth = algorithm.get_ground_truth(data)
    expected_ground_truth = np.array([1, 1, 0, 0])
    assert ground_truth.shape == expected_ground_truth.shape
    for i in range(expected_ground_truth.shape[0]):
        assert math.isclose(ground_truth[i], expected_ground_truth[i], abs_tol=1e-5)
