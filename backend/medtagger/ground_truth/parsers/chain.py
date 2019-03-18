"""Definition of parser for Chain Label Elements."""
from typing import List

import numpy as np
from PIL import Image
from skimage import draw

from medtagger.database import models
from medtagger.ground_truth.parsers import base


class ChainLabelElementParser(base.LabelElementParser):
    """Parser for Chain Label Element."""

    DEFAULT_WIDTH = 512
    DEFAULT_HEIGHT = 512
    IMAGE_AFTER_RESHAPE = (100, 100)

    def convert_to_numpy(self, label_elements: List[models.ChainLabelElement], resize_image: bool = False) \
            -> np.ndarray:
        """Convert given list of Chain Label Elements to numpy array.

        :param label_elements: list of Chain Label Elements that should be converted
        :param resize_image: (optional) should parser resize the image down for easier Ground Truth generation
        :return: numpy representation of a given Chain Label Elements
        """
        masks = []
        for element in label_elements:
            scan_width = element.label.scan.width or self.DEFAULT_WIDTH
            scan_height = element.label.scan.height or self.DEFAULT_HEIGHT
            mask = np.zeros((scan_width, scan_height), 'uint8')
            poly = np.array([(p.x * scan_width, p.y * scan_height) for p in element.points])
            rr, cc = draw.polygon(poly[:, 1], poly[:, 0], mask.shape)
            mask[rr, cc] = 1.0
            masks.append(mask)

        # Some methods require to resize images in order to properly generate Ground Truth data set
        # It is mostly required due to performance reasons (e.g. DBSCAN or K-Means)
        if resize_image:
            resized_masks = np.array([np.array(Image.fromarray(mask).resize(self.IMAGE_AFTER_RESHAPE))
                                      for mask in masks])
        else:
            resized_masks = np.array(masks)

        # A lot of methods does not work in more than 2 dimensions, so let's just flatten it
        desired_shape = (resized_masks.shape[0], resized_masks.shape[1] * resized_masks.shape[2])
        all_masks_flattened = np.reshape(resized_masks, desired_shape)
        return all_masks_flattened

    def compute_intersection_over_union(self, first_label_element: np.ndarray, second_label_element: np.ndarray) \
            -> float:
        """Compute metric for Intersection over Union (IoU).

        :param first_label_element: first Label Element as numpy array
        :param second_label_element: second Label Element as numpy array
        :return: floating point IoU measure
        """
        intersection = np.sum(first_label_element * second_label_element)
        sum_of_two_labels = first_label_element + second_label_element
        sum_of_two_labels[sum_of_two_labels >= 1.0] = 1.0  # Removes overlapping
        union = np.sum(sum_of_two_labels)
        return intersection / union
