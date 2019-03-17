import abc

import numpy as np


class GeneratorAlgorithm(abc.ABC):

    require_image_resize = False

    def __init__(self) -> None:
        pass

    def get_ground_truth(self, data: np.ndarray) -> np.ndarray:
        raise NotImplementedError
