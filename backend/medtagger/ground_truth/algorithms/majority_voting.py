"""Definition of a Majority Voting Algorithm."""
import numpy as np

from scipy.spatial import distance

from medtagger.ground_truth.algorithms.base import GeneratorAlgorithm


class MajorityVotingAlgorithm(GeneratorAlgorithm):  # pylint: disable=too-few-public-methods
    """Majority Voting Algorithm implementation."""

    REQUIRE_IMAGE_RESIZE = False

    def get_ground_truth(self, data: np.ndarray) -> np.ndarray:
        """Calculate output Ground Truth label using Majority Voting algorithm.

        :param data: numpy representation of list of Label Elements that needs to processed
        :return: numpy array with a single Ground Truth label
        """
        distance_between_all_points = distance.cdist(data, data)
        total_distance_for_each_point = distance_between_all_points.sum(axis=0)
        best_points_sorted = np.argsort(total_distance_for_each_point)
        half_of_points = max(1, int(data.shape[0] / 2))
        majority_of_best_points = np.take(data, best_points_sorted[:half_of_points], axis=0)
        return np.mean(majority_of_best_points, axis=0)
