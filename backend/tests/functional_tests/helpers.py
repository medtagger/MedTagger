"""Helpers functions for functional tests."""
from typing import List, Tuple

from medtagger import definitions
from medtagger.types import LabelingTime
from medtagger.database import models
from medtagger.repositories import (
    datasets as DatasetsRepository,
    labels as LabelsRepository,
    label_tags as LabelTagsRepository,
    scans as ScansRepository,
    tasks as TasksRepository,
)


def create_tag_and_assign_to_task(key: str, name: str, task_key: str, tools: List[models.LabelTool]) -> models.LabelTag:
    """Create Label Tag and assign it to Task.

    :param key: key that will identify such Label Tag
    :param name: name that will be used in the User Interface for such Label Tag
    :param task_key: key of the Task that Label Tag will be assigned to
    :param tools: list of tools for given Label Tag that will be available on labeling page
    :return: Label Tag
    """
    label_tag = models.LabelTag(key, name, tools)
    TasksRepository.assign_label_tag(label_tag, task_key)
    return label_tag


def prepare_scan_and_tag_for_labeling() -> Tuple[models.Scan, models.LabelTag]:
    """Create needed Scan and Label Tag for labeling purpose."""
    dataset = DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    task = TasksRepository.add_task('MARK_KIDNEYS', 'Mark Kidneys', 'path/to/image', ['KIDNEYS'], '', [], [])
    label_tag = LabelTagsRepository.add_new_tag('EXAMPLE_TAG', 'Example Tag', [definitions.LabelTool.POINT], task.id)
    scan = ScansRepository.add_new_scan(dataset, number_of_slices=3)
    for _ in range(3):
        scan.add_slice()
    return scan, label_tag


def prepare_empty_label(scan: models.Scan, user: models.User) -> models.Label:
    """Create empty Label for given Scan and User."""
    return LabelsRepository.add_new_label(scan.id, 'MARK_KIDNEYS', user, LabelingTime(0.0))
