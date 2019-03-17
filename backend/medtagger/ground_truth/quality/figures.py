from typing import Dict, List

import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import func
from sklearn import linear_model

from medtagger.database import models


def specificity_vs_sensitivity(users_specificity: Dict[str, np.ndarray], users_sensitivity: Dict[str, np.ndarray]) -> None:
    plt.figure()
    plt.title('Specificity vs. Sensitivity')
    plt.scatter(1 - np.array(list(users_specificity.values())), np.array(list(users_sensitivity.values())))
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xlabel('1 - Specificity')
    plt.ylabel('Sensitivity')
    plt.show()


def mean_labeling_time_vs_score(label_elements: List[models.LabelElement], users_scores: Dict[str, np.ndarray]) -> None:
    scans_ids = {label_element.label.scan_id for label_element in label_elements}
    query = models.Label.query.with_entities(models.Label.owner_id, func.avg(models.Label.labeling_time))
    query = query.filter(models.Label.scan_id.in_(scans_ids)).group_by(models.Label.owner_id)
    labeling_time_for_user_id = dict(query.all())

    user_ids = list(users_scores.keys())
    scores = [users_scores.get(user_id, 0) for user_id in user_ids]
    labeling_time = [labeling_time_for_user_id.get(user_id, 0) for user_id in user_ids]

    linear_regression = linear_model.LinearRegression().fit(np.array(labeling_time)[:, None], scores)
    x = np.arange(min(labeling_time), max(labeling_time), 1)
    plt.figure()
    plt.plot(x, x * linear_regression.coef_[0] + linear_regression.intercept_, "r--")
    plt.title('Mean Labeling Time vs. Score')
    plt.scatter(labeling_time, scores)
    plt.xlabel('Mean Labeling Time')
    plt.ylabel('Score')
    plt.ylim(0, 1)
    plt.show()
