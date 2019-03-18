"""Ground Truth generator class."""
import collections
from typing import List, Dict

import numpy as np

from medtagger.types import SliceID
from medtagger.database import models
from medtagger.repositories import slices as SlicesRepository
from medtagger.ground_truth import parsers
from medtagger.ground_truth.algorithms.base import GeneratorAlgorithm


class DataSetGenerator:
    """Generator for the Ground Truth data set based on entered labels."""  # pylint: disable=too-few-public-methods

    def __init__(self, algorithm: GeneratorAlgorithm) -> None:
        """Initialize generator with given algorithm.

        :param algorithm: algorithm object which should be used during data set generation
        """
        self.algorithm = algorithm

    def generate(self, label_elements: List[models.LabelElement]) -> Dict[SliceID, np.ndarray]:
        """Generate final Ground Truth data set.

        :param label_elements: list of all Label Elements that should be taken into consideration during generation
        :return: Ground Truth label for each Slice ID in labelled Scans
        """
        label_elements_for_slice_id: Dict[SliceID, List[models.LabelElement]] = collections.defaultdict(list)
        for label_element in label_elements:
            labeled_slice = label_element.label.scan.slices[label_element.slice_index]
            label_elements_for_slice_id[labeled_slice.id].append(label_element)

        ground_truth_per_slice_id: Dict[SliceID, np.ndarray] = {}
        slices_ids = SlicesRepository.get_slices_ids_for_labeled_scans(label_elements)
        for slice_id in slices_ids:
            label_elements = label_elements_for_slice_id[slice_id]
            if len(label_elements) < 2:
                ground_truth_per_slice_id[slice_id] = None
                continue  # Doesn't make any sense to analyse < 2 elements

            parser = parsers.get_parser(type(label_elements[0]))
            data = parser.convert_to_numpy(label_elements, self.algorithm.REQUIRE_IMAGE_RESIZE)
            ground_truth_per_slice_id[slice_id] = self.algorithm.get_ground_truth(data)
        return ground_truth_per_slice_id
