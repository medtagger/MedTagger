"""Definition of a DBSCAN Algorithm."""
import collections

import numpy as np
from sklearn import cluster

from medtagger.ground_truth.algorithms.base import GeneratorAlgorithm


class DBSCANAlgorithm(GeneratorAlgorithm):  # pylint: disable=too-few-public-methods
    """DBSCAN Algorithm implementation."""

    REQUIRE_IMAGE_RESIZE = False
    NOISE_LABEL = -1

    # NOTE: Find better parameters automatically
    EPS = 0.5
    MIN_SAMPLES = 2

    def get_ground_truth(self, data: np.ndarray) -> np.ndarray:
        """Calculate output Ground Truth label using DBSCAN algorithm.

        :param data: numpy representation of list of Label Elements that needs to processed
        :return: numpy array with a single Ground Truth label
        """
        model = cluster.DBSCAN(eps=self.EPS, min_samples=self.MIN_SAMPLES)
        model.fit(data)

        # In case all Labels were marked as noise - take non-existing label (0)
        labels = [label for label in model.labels_ if label != self.NOISE_LABEL] or [0]
        most_common_cluster = collections.Counter(labels).most_common(1)[0][0]
        best_points_idx = {idx for idx in model.core_sample_indices_ if model.labels_[idx] == most_common_cluster}
        best_points_idx = best_points_idx or {0}  # In case all Labels were noise - let's use first Label Element
        best_points = [data[idx] for idx in best_points_idx]
        return np.mean(best_points, axis=0)
