from typing import List

import numpy as np

from medtagger.database import models
from medtagger.ground_truth.parsers.base import GeneratorParser


class RectangleParser(GeneratorParser):

    def __init__(self) -> None:
        super(RectangleParser, self).__init__()

    def convert_to_numpy(self, label_elements: List[models.RectangularLabelElement], resize: bool = False) -> np.ndarray:
        return np.array([[e.x, e.y, e.x + e.width, e.y + e.height] for e in label_elements])

    def compute_intersection_over_union(self, first_label_element: np.ndarray, second_label_element: np.ndarray) -> float:
        intersection_width = max(0, min(first_label_element[2], second_label_element[2]) - max(first_label_element[0], second_label_element[0]))
        intersection_height = max(0, min(first_label_element[3], second_label_element[3]) - max(first_label_element[1], second_label_element[1]))
        intersection = intersection_width * intersection_height
        union = ((first_label_element[2] - first_label_element[0]) * (first_label_element[3] - first_label_element[1]) +
                 (second_label_element[2] - second_label_element[0]) * (second_label_element[3] - second_label_element[1]))
        return intersection / union
