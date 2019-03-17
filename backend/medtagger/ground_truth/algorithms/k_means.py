"""Definition of a K-Means Algorithm."""
import collections

import numpy as np
from sklearn import cluster

from medtagger.ground_truth.algorithms.base import GeneratorAlgorithm


class KMeansAlgorithm(GeneratorAlgorithm):
    """K-Means Algorithm implementation."""

    REQUIRE_IMAGE_RESIZE = True
    MAX_NUMBER_OF_CLUSTERS = 5

    def __init__(self) -> None:
        """Initialize algorithm."""
        super(KMeansAlgorithm, self).__init__()

    def get_ground_truth(self, data: np.ndarray) -> np.ndarray:
        """Calculate output Ground Truth label using K-Means algorithm.

        :param data: numpy representation of list of Label Elements that needs to processed
        :return: numpy array with a single Ground Truth label
        """
        number_of_clusters = self._choose_number_of_clusters(data)
        model = cluster.KMeans(n_clusters=number_of_clusters)
        model.fit(data)
        most_common_cluster = collections.Counter(model.labels_).most_common(1)
        return model.cluster_centers_[most_common_cluster[0][0]]

    def _choose_number_of_clusters(self, data: np.ndarray) -> int:
        """Calculate the best number of clusters based on passed data.

        This method uses bend (or knee) location approach to find the best number of clusters.
        It looks for the number of clusters that has the most difference in inertia level.

        :param data: numpy representation of list of Label Elements that needs to processed
        :return: number of clusters that should be used and will work best for given data
        """
        previous_difference = 0
        for number_of_clusters in range(1, min(self.MAX_NUMBER_OF_CLUSTERS, data.shape[0]) + 1):
            model = cluster.KMeans(n_clusters=number_of_clusters)
            model.fit(data)
            current_difference = model.inertia_ - previous_difference
            if previous_difference < current_difference:
                return number_of_clusters
            previous_difference = current_difference
        return min(self.MAX_NUMBER_OF_CLUSTERS, data.shape[0])
