"""Definition of base class for all algorithms."""
import abc

import numpy as np


class GeneratorAlgorithm(abc.ABC):
    """Base abstract class for all algorithms."""

    REQUIRE_IMAGE_RESIZE = False

    def __init__(self) -> None:
        """Initialize algorithm."""
        pass

    def get_ground_truth(self, data: np.ndarray) -> np.ndarray:
        """Calculate output Ground Truth label using some algorithm.

        :param data: numpy representation of list of Label Elements that needs to processed
        :return: numpy array with a single Ground Truth label
        """
        raise NotImplementedError
