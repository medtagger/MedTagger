"""Definition of a Gaussian Mixture Models Algorithm."""
import numpy as np
from sklearn import mixture

from medtagger.ground_truth.algorithms.base import GeneratorAlgorithm


class GaussianMixtureModelsAlgorithm(GeneratorAlgorithm):
    """Gaussian Mixture Models Algorithm implementation."""

    REQUIRE_IMAGE_RESIZE = True
    MAX_NUMBER_OF_COMPONENTS = 5

    INIT_PARAMS = 'random'
    REG_COVAR = 1e-2
    COVARIANCE_TYPE = 'spherical'

    def __init__(self) -> None:
        """Initialize algorithm."""
        super(GaussianMixtureModelsAlgorithm, self).__init__()

    def get_ground_truth(self, data: np.ndarray) -> np.ndarray:
        """Calculate output Ground Truth label using Gaussian Mixture Models algorithm.

        :param data: numpy representation of list of Label Elements that needs to processed
        :return: numpy array with a single Ground Truth label
        """
        number_of_components = self._choose_number_of_components(data)
        model = mixture.GaussianMixture(n_components=number_of_components, init_params=self.INIT_PARAMS,
                                        reg_covar=self.REG_COVAR, covariance_type=self.COVARIANCE_TYPE)
        model.fit(data)
        best_component = model.weights_.argmax()
        return model.means_[best_component]

    def _choose_number_of_components(self, data: np.ndarray) -> int:
        """Calculate the best number of components based on passed data.

        This method uses Bayesian Information Criterion (BIC) in order to find the last
        number of components that has the most impact on data fitness.

        :param data: numpy representation of list of Label Elements that needs to processed
        :return: number of components that should be used and will work best for given data
        """
        previous_bic_value = 0
        for components in range(1, min(self.MAX_NUMBER_OF_COMPONENTS, data.shape[0]) + 1):
            model = mixture.GaussianMixture(n_components=components, init_params=self.INIT_PARAMS,
                                            reg_covar=self.REG_COVAR, covariance_type=self.COVARIANCE_TYPE)
            model.fit(data)
            value = model.bic(data)
            if value > previous_bic_value:
                return components - 1  # Previous component was better, so let's use it
            previous_bic_value = value
        return min(self.MAX_NUMBER_OF_COMPONENTS, data.shape[0])

