"""Definition of a base class for Label Element Parser."""
import abc
from typing import List

import numpy as np

from medtagger.database import models


class LabelElementParser(abc.ABC):
    """Base abstract class for all parsers."""

    def convert_to_numpy(self, label_elements: List[models.LabelElement], resize_image: bool = False) -> np.ndarray:
        """Convert given list of Label Elements to numpy array.

        :param label_elements: list of Label Elements that should be converted
        :param resize_image: (optional) should parser resize the image down for easier Ground Truth generation
        :return: numpy representation of a given Label Elements
        """
        raise NotImplementedError

    def compute_intersection_over_union(self, first_label_element: np.ndarray, second_label_element: np.ndarray) \
            -> float:
        """Compute metric for Intersection over Union (IoU).

        :param first_label_element: first Label Element as numpy array
        :param second_label_element: second Label Element as numpy array
        :return: floating point IoU measure
        """
        raise NotImplementedError
