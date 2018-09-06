"""Tests Labels Repository."""
import json
from typing import Any

from medtagger.storage.models import BrushLabelElement
from medtagger.database.models import User
from medtagger.definitions import LabelTool
from medtagger.repositories import (
    datasets as DatasetsRepository,
    label_tags as LabelTagsRepository,
    tasks as TasksRepository,
    scans as ScansRepository,
    labels as LabelsRepository,
    users as UsersRepository,
)
from medtagger.types import LabelingTime

from tests.functional_tests.conftest import get_token_for_logged_in_user


def test_get_predefined_label_for_scan_in_task__no_predefined_label(prepare_environment: Any) -> None:
    """Test for fetching Predefined Label that does not exist."""
    # Step 1. Prepare a structure for the test
    dataset = DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    task = TasksRepository.add_task('MARK_KIDNEYS', 'Mark Kidneys', 'path/to/image', ['KIDNEYS'], [])
    LabelTagsRepository.add_new_tag('EXAMPLE_TAG', 'Example Tag', [LabelTool.RECTANGLE], task.id)
    scan = ScansRepository.add_new_scan(dataset, 0)

    # Step 2. Check if there is no Predefined Label
    predefined_label = LabelsRepository.get_predefined_label_for_scan_in_task(scan, task)
    assert not predefined_label


def test_get_predefined_label_for_scan_in_task__label_that_is_not_predefined(prepare_environment: Any) -> None:
    """Test for fetching Predefined Label that is not predefined."""
    # Step 1. Prepare a structure for the test
    dataset = DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    task = TasksRepository.add_task('MARK_KIDNEYS', 'Mark Kidneys', 'path/to/image', ['KIDNEYS'], [])
    LabelTagsRepository.add_new_tag('EXAMPLE_TAG', 'Example Tag', [LabelTool.RECTANGLE], task.id)
    scan = ScansRepository.add_new_scan(dataset, 0)
    user_id = UsersRepository.add_new_user(User('user@medtagger', 'HASH', 'Admin', 'Admin'))
    user = UsersRepository.get_user_by_id(user_id)

    # Step 2. Add Label which is not predefined
    LabelsRepository.add_new_label(scan.id, task.key, user, LabelingTime(0), predefined=False)

    # Step 3. Check if there is no Predefined Label
    predefined_label = LabelsRepository.get_predefined_label_for_scan_in_task(scan, task)
    assert not predefined_label


def test_get_predefined_label_for_scan_in_task__predefined_label(prepare_environment: Any) -> None:
    """Test for fetching Predefined Label that exists."""
    # Step 1. Prepare a structure for the test
    dataset = DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    task = TasksRepository.add_task('MARK_KIDNEYS', 'Mark Kidneys', 'path/to/image', ['KIDNEYS'], [])
    LabelTagsRepository.add_new_tag('EXAMPLE_TAG', 'Example Tag', [LabelTool.RECTANGLE], task.id)
    scan = ScansRepository.add_new_scan(dataset, 0)
    user_id = UsersRepository.add_new_user(User('user@medtagger', 'HASH', 'Admin', 'Admin'))
    user = UsersRepository.get_user_by_id(user_id)

    # Step 2. Add Label which is predefined
    label = LabelsRepository.add_new_label(scan.id, task.key, user, LabelingTime(0), predefined=True)

    # Step 3. Check if there is is Predefined Label
    predefined_label = LabelsRepository.get_predefined_label_for_scan_in_task(scan, task)
    assert predefined_label.id == label.id


def test_get_predefined_label_for_scan_in_task__predefined_label_for_given_task(prepare_environment: Any) -> None:
    """Test for fetching Predefined Label only for specific Task."""
    # Step 1. Prepare a structure for the test
    dataset = DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    task_left = TasksRepository.add_task('MARK_LEFT', 'Mark Left', 'path/to/image', ['KIDNEYS'], [])
    task_right = TasksRepository.add_task('MARK_RIGHT', 'Mark Right', 'path/to/image', ['KIDNEYS'], [])
    LabelTagsRepository.add_new_tag('EXAMPLE_TAG', 'Example Tag', [LabelTool.RECTANGLE], task_left.id)
    scan = ScansRepository.add_new_scan(dataset, 0)
    user_id = UsersRepository.add_new_user(User('user@medtagger', 'HASH', 'Admin', 'Admin'))
    user = UsersRepository.get_user_by_id(user_id)

    # Step 2. Add Labels for each Task
    label_left = LabelsRepository.add_new_label(scan.id, task_left.key, user, LabelingTime(0), predefined=True)
    label_right = LabelsRepository.add_new_label(scan.id, task_right.key, user, LabelingTime(0), predefined=True)

    # Step 3. Check if there are these Predefined Labels
    predefined_label = LabelsRepository.get_predefined_label_for_scan_in_task(scan, task_left)
    assert predefined_label.id == label_left.id
    predefined_label = LabelsRepository.get_predefined_label_for_scan_in_task(scan, task_right)
    assert predefined_label.id == label_right.id


def test_get_predefined_brush_label_elements(prepare_environment: Any) -> None:
    """Test for fetching Predefined Brush Label Elements."""
    # Step 1. Prepare a structure for the test
    dataset = DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    task = TasksRepository.add_task('MARK_KIDNEYS', 'Mark Kidneys', 'path/to/image', ['KIDNEYS'], [])
    label_tag = LabelTagsRepository.add_new_tag('EXAMPLE_TAG', 'Example Tag', [LabelTool.RECTANGLE], task.id)
    scan = ScansRepository.add_new_scan(dataset, 3)
    user_id = UsersRepository.add_new_user(User('user@medtagger', 'HASH', 'Admin', 'Admin'))
    user = UsersRepository.get_user_by_id(user_id)

    # Step 2. Add Label with Brush Elements
    label = LabelsRepository.add_new_label(scan.id, task.key, user, LabelingTime(0), predefined=True)
    LabelsRepository.add_new_brush_label_element(label.id, 0, 0, 0, b'', label_tag)
    LabelsRepository.add_new_brush_label_element(label.id, 1, 0, 0, b'', label_tag)
    LabelsRepository.add_new_brush_label_element(label.id, 2, 0, 0, b'', label_tag)

    # Step 3. Check if there is is Predefined Label
    brush_label_elements = LabelsRepository.get_predefined_brush_label_elements(scan.id, task.id, 0, 3)
    assert len(brush_label_elements) == 3
    brush_label_elements = LabelsRepository.get_predefined_brush_label_elements(scan.id, task.id, 0, 1)
    assert len(brush_label_elements) == 1
