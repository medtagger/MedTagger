import abc
from typing import List

import numpy as np

from medtagger.database import models


class GeneratorParser(abc.ABC):

    def __init__(self) -> None:
        pass

    def convert_to_numpy(self, label_elements: List[models.LabelElement], resize: bool = False) -> np.ndarray:
        raise NotImplementedError

    def compute_intersection_over_union(self, label_element_a: np.ndarray, label_element_b: np.ndarray) -> float:
        raise NotImplementedError
