"""Definition of parser for Rectangular Label Elements."""
from typing import List

import numpy as np

from medtagger.database import models
from medtagger.ground_truth.parsers import base


class RectangleLabelElementParser(base.LabelElementParser):
    """Parser for Rectangular Label Element."""

    def convert_to_numpy(self, label_elements: List[models.RectangularLabelElement], resize_image: bool = False) \
            -> np.ndarray:
        """Convert given list of Rectangular Label Elements to numpy array.

        :param label_elements: list of Rectangular Label Elements that should be converted
        :param resize_image: (optional) should parser resize the image down for easier Ground Truth generation
        :return: numpy representation of a given Rectangular Label Elements
        """
        return np.array([[e.x, e.y, e.x + e.width, e.y + e.height] for e in label_elements])

    def compute_intersection_over_union(self, first_label_element: np.ndarray, second_label_element: np.ndarray) \
            -> float:
        """Compute metric for Intersection over Union (IoU).

        :param first_label_element: first Label Element as numpy array
        :param second_label_element: second Label Element as numpy array
        :return: floating point IoU measure
        """  # pylint: disable=too-many-locals  # Many locals increase readability in this place
        max_x1 = max(first_label_element[0], second_label_element[0])
        max_y1 = max(first_label_element[1], second_label_element[1])
        min_x2 = min(first_label_element[2], second_label_element[2])
        min_y2 = min(first_label_element[3], second_label_element[3])

        intersection_width = max(0, min_x2 - max_x1)
        intersection_height = max(0, min_y2 - max_y1)
        intersection = intersection_width * intersection_height

        first_width = first_label_element[2] - first_label_element[0]
        first_height = first_label_element[3] - first_label_element[1]
        second_width = second_label_element[2] - second_label_element[0]
        second_height = second_label_element[3] - second_label_element[1]

        first_label_field = first_width * first_height
        second_label_field = second_width * second_height
        union = first_label_field + second_label_field - intersection

        return intersection / union
