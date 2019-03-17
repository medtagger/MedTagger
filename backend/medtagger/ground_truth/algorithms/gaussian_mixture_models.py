import numpy as np
from sklearn import mixture

from medtagger.ground_truth.algorithms.base import GeneratorAlgorithm


class GaussianMixtureModelsAlgorithm(GeneratorAlgorithm):

    require_image_resize = True

    def __init__(self) -> None:
        super(GaussianMixtureModelsAlgorithm, self).__init__()

    def get_ground_truth(self, data: np.ndarray) -> np.ndarray:
        number_of_components = self._choose_number_of_components(data)
        model = mixture.GaussianMixture(n_components=number_of_components, init_params='random',
                                        reg_covar=1e-2, covariance_type='spherical')
        model.fit(data)
        best_component = model.weights_.argmax()
        return model.means_[best_component]

    def _choose_number_of_components(self, data: np.ndarray) -> int:
        prev_value = 0
        for components in range(1, data.shape[0] + 1):
            model = mixture.GaussianMixture(n_components=components, init_params='random',
                                            reg_covar=1e-2, covariance_type='spherical')
            model.fit(data)
            value = model.bic(data)
            if value > prev_value:
                return components - 1  # Previous component was better
            prev_value = value
        return data.shape[0]

