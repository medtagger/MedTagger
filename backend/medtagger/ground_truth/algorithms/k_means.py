import collections

import numpy as np
from sklearn import cluster

from medtagger.ground_truth.algorithms.base import GeneratorAlgorithm


class KMeansAlgorithm(GeneratorAlgorithm):

    require_image_resize = True
    MAX_NUMBER_OF_CLUSTERS = 5

    def __init__(self) -> None:
        super(KMeansAlgorithm, self).__init__()

    def get_ground_truth(self, data: np.ndarray) -> np.ndarray:
        number_of_clusters = self._choose_number_of_clusters(data)
        model = cluster.KMeans(n_clusters=number_of_clusters)
        model.fit(data)
        most_common_cluster = collections.Counter(model.labels_).most_common(1)
        return model.cluster_centers_[most_common_cluster[0][0]]

    def _choose_number_of_clusters(self, data: np.ndarray) -> int:
        inertia_for_clusters = []
        for clusters in range(1, min(self.MAX_NUMBER_OF_CLUSTERS, data.shape[0] + 1)):
            model = cluster.KMeans(n_clusters=clusters)
            model.fit(data)
            inertia_for_clusters.append(model.inertia_)

        prev_diff = inertia_for_clusters[0]
        for i in range(len(inertia_for_clusters) - 1):
            current_diff = inertia_for_clusters[i + 1] - inertia_for_clusters[i]
            if prev_diff < current_diff:
                return i + 1
            prev_diff = current_diff
        return len(inertia_for_clusters)
