import numpy as np
from sklearn import cluster

from medtagger.ground_truth.algorithms.base import GeneratorAlgorithm


class DBSCANAlgorithm(GeneratorAlgorithm):

    require_image_resize = False

    def __init__(self) -> None:
        super(DBSCANAlgorithm, self).__init__()

    def get_ground_truth(self, data: np.ndarray) -> np.ndarray:
        model = cluster.DBSCAN(eps=0.5, min_samples=2)  # TODO: Find better parameters
        model.fit(data)

        unique_cluster_ids = {model.labels_[idx] for idx in model.core_sample_indices_}
        best_cluster, _best_cluster_number_of_points = None, None
        for cluster_id in unique_cluster_ids:
            number_of_points = len([True for label in model.labels_ if label == cluster_id])
            if best_cluster is None or number_of_points > _best_cluster_number_of_points:
                _best_cluster_number_of_points = number_of_points
                best_cluster = cluster_id
        best_points_idx = {idx for idx in model.core_sample_indices_ if model.labels_[idx] == best_cluster}
        best_points_idx = best_points_idx or {0}  # In case all Labels were marked as noise - let's take first one
        best_points = [data[idx] for idx in best_points_idx]
        return np.mean(best_points, axis=0)
