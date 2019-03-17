import numpy as np

from medtagger.ground_truth.algorithms.base import GeneratorAlgorithm


class MajorityVotingAlgorithm(GeneratorAlgorithm):

    require_image_resize = False

    def __init__(self) -> None:
        super(MajorityVotingAlgorithm, self).__init__()

    def get_ground_truth(self, data: np.ndarray) -> np.ndarray:
        return np.mean(data, axis=0)
