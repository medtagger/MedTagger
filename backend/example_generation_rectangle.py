from pprint import pprint

from medtagger.database import models
from medtagger.ground_truth.algorithms.dbscan import DBSCANAlgorithm
from medtagger.ground_truth.algorithms.k_means import KMeansAlgorithm
from medtagger.ground_truth.algorithms.majority_voting import MajorityVotingAlgorithm
from medtagger.ground_truth.algorithms.gaussian_mixture_models import GaussianMixtureModelsAlgorithm
from medtagger.ground_truth.generator import DataSetGenerator
from medtagger.ground_truth.quality import figures
from medtagger.ground_truth.quality.user_specificity_sensitivity import compute_specificity_and_sensitivity_for_users


algorithm = DBSCANAlgorithm()
generator = DataSetGenerator(algorithm)

scans = models.Scan.query.all()
scans_ids = {scan.id for scan in scans}

query = models.RectangularLabelElement.query.join(models.Label)
query = query.filter(models.Label.scan_id.in_(scans_ids))
rectangular_label_elements = query.all()

ground_truth = generator.generate(rectangular_label_elements)
print('Ground Truth:')
pprint(ground_truth)

users = set(element.label.owner for element in rectangular_label_elements)
users_specificity, users_sensitivity, users_scores = compute_specificity_and_sensitivity_for_users(
    algorithm, users, rectangular_label_elements, ground_truth)

users_ids = set(e.label.owner_id for e in rectangular_label_elements)
for user_id in users_ids:
    print('User:', user_id, ' \n',
          'Sensitivity:', users_sensitivity[user_id], ' \n',
          'Specificity:', users_specificity[user_id], ' \n',
          'Score:', users_scores[user_id], ' \n')

figures.specificity_vs_sensitivity(users_specificity, users_sensitivity)
figures.mean_labeling_time_vs_score(rectangular_label_elements, users_scores)
