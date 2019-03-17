"""Definition of a Majority Voting Algorithm."""
import numpy as np

from medtagger.ground_truth.algorithms.base import GeneratorAlgorithm


class MajorityVotingAlgorithm(GeneratorAlgorithm):
    """Majority Voting Algorithm implementation."""

    REQUIRE_IMAGE_RESIZE = False

    def __init__(self) -> None:
        """Initialize algorithm."""
        super(MajorityVotingAlgorithm, self).__init__()

    def get_ground_truth(self, data: np.ndarray) -> np.ndarray:
        """Calculate output Ground Truth label using Majority Voting algorithm.

        :param data: numpy representation of list of Label Elements that needs to processed
        :return: numpy array with a single Ground Truth label
        """
        return np.mean(data, axis=0)
