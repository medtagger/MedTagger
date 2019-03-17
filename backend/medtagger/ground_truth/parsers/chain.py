from typing import List

import numpy as np
from PIL import Image
from skimage import draw

from medtagger.database import models
from medtagger.ground_truth.parsers.base import GeneratorParser


class ChainParser(GeneratorParser):

    RESIZED_SHAPE = (100, 100)

    def __init__(self) -> None:
        super(ChainParser, self).__init__()

    def convert_to_numpy(self, label_elements: List[models.ChainLabelElement], resize: bool = False) -> np.ndarray:
        masks = []
        for element in label_elements:
            mask = np.zeros((element.label.scan.width, element.label.scan.height), 'uint8')
            poly = np.array([(p.x * element.label.scan.width, p.y * element.label.scan.height) for p in element.points])
            rr, cc = draw.polygon(poly[:, 1], poly[:, 0], mask.shape)
            mask[rr, cc] = 1.0
            masks.append(mask)

        # Some methods needs to resize images in order to properly generate Ground Truth data set
        if resize:
            resized_masks = np.array([np.array(Image.fromarray(mask).resize(self.RESIZED_SHAPE)) for mask in masks])
        else:
            resized_masks = np.array(masks)
        desired_shape = (resized_masks.shape[0], resized_masks.shape[1] * resized_masks.shape[2])
        all_masks_flattened = np.reshape(resized_masks, desired_shape)
        return all_masks_flattened

    def compute_intersection_over_union(self, label_element_a: np.ndarray, label_element_b: np.ndarray) -> float:
        intersection = np.sum(label_element_a * label_element_b)
        sum_of_two_labels = label_element_a + label_element_b
        sum_of_two_labels[sum_of_two_labels >= 1.0] = 1.0
        union = np.sum(sum_of_two_labels)
        return intersection / union
