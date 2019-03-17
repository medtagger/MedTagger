import collections
from typing import List, Dict

import numpy as np

from medtagger.database import models
from medtagger.ground_truth import parsers
from medtagger.ground_truth.algorithms.base import GeneratorAlgorithm


class DataSetGenerator:

    def __init__(self, algorithm: GeneratorAlgorithm) -> None:
        self.algorithm = algorithm

    def generate(self, label_elements: List[models.LabelElement]) -> Dict[str, np.ndarray]:
        labels_for_slice_id = collections.defaultdict(list)
        for label_element in label_elements:
            labeled_slice = label_element.label.scan.slices[label_element.slice_index]
            labels_for_slice_id[labeled_slice.id].append(label_element)

        scans_ids = {label_element.label.scan_id for label_element in label_elements}
        slices = models.Slice.query.with_entities(models.Slice.id).filter(models.Slice.scan_id.in_(scans_ids)).all()
        slices_ids = {_slice.id for _slice in slices}

        ground_truth_per_slice_id = {}
        for slice_id in slices_ids:
            label_elements = labels_for_slice_id[slice_id]
            if len(label_elements) < 2:
                ground_truth_per_slice_id[slice_id] = None
                continue  # Skipping as it doesn't make any sense to analyse <2 elements...

            parser = parsers.get_parser(type(label_elements[0]))
            data = parser.convert_to_numpy(label_elements, self.algorithm.require_image_resize)
            ground_truth_per_slice_id[slice_id] = self.algorithm.get_ground_truth(data)

        return ground_truth_per_slice_id
