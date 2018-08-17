"""Tests for adding new Labels to the system."""
from typing import Any

import yaml

from medtagger.repositories import (
    datasets as DatasetsRepository,
    tasks as TasksRepository,
    label_tags as LabelTagsRepository,
)
from scripts import sync_configuration as script


def test_sync_with_empty_database(prepare_environment: Any) -> None:
    """Test for configuration synchronization with empty database."""
    configuration = yaml.load("""
        datasets:
          - key: KIDNEYS
            name: Kidneys
            tasks:
              - KIDNEYS_SEGMENTATION

        tasks:
          - key: KIDNEYS_SEGMENTATION
            name: Kidneys segmentation
            image_path: assets/icon/kidneys_dataset_icon.svg
            tags:
              - key: LEFT_KIDNEY
                name: Left Kidney
                tools:
                  - CHAIN
                  - BRUSH
              - key: RIGHT_KIDNEY
                name: Right Kidney
                tools:
                  - CHAIN
    """)
    script.sync_configuration(configuration)

    # Check if Datasets were synchronized properly
    datasets = DatasetsRepository.get_all_datasets(include_disabled=True)
    assert len(datasets) == 1
    kidneys = DatasetsRepository.get_dataset_by_key('KIDNEYS')
    assert kidneys.name == 'Kidneys'
    assert not kidneys.disabled
    assert {task.key for task in kidneys.tasks} == {'KIDNEYS_SEGMENTATION'}

    # Check if Tasks were synchronized properly
    tasks = TasksRepository.get_all_tasks(include_disabled=True)
    assert len(tasks) == 1
    kidneys_segmentation = TasksRepository.get_task_by_key('KIDNEYS_SEGMENTATION')
    assert kidneys_segmentation.name == 'Kidneys segmentation'
    assert kidneys_segmentation.image_path == 'assets/icon/kidneys_dataset_icon.svg'
    assert not kidneys_segmentation.disabled
    assert len(kidneys_segmentation.available_tags) == 2
    assert {tag.key for tag in kidneys_segmentation.available_tags} == {'LEFT_KIDNEY', 'RIGHT_KIDNEY'}

    # Check if Label Tags were synchronized properly
    tags = LabelTagsRepository.get_all_tags(include_disabled=True)
    assert len(tags) == 2
    left_kidney = LabelTagsRepository.get_label_tag_by_key('LEFT_KIDNEY')
    assert left_kidney.name == 'Left Kidney'
    assert not left_kidney.disabled
    assert {tool.name for tool in left_kidney.tools} == {'CHAIN', 'BRUSH'}
    right_kidney = LabelTagsRepository.get_label_tag_by_key('RIGHT_KIDNEY')
    assert right_kidney.name == 'Right Kidney'
    assert not right_kidney.disabled
    assert {tool.name for tool in right_kidney.tools} == {'CHAIN'}


def test_sync_with_updated_names(prepare_environment: Any) -> None:
    """Test for configuration synchronization with updated names."""
    configuration = yaml.load("""
        datasets:
          - key: KIDNEYS
            name: Kidneys
            tasks:
              - KIDNEYS_SEGMENTATION

        tasks:
          - key: KIDNEYS_SEGMENTATION
            name: Kidneys segmentation
            image_path: assets/icon/kidneys_dataset_icon.svg
            tags:
              - key: LEFT_KIDNEY
                name: Left Kidney
                tools:
                  - CHAIN
                  - BRUSH
              - key: RIGHT_KIDNEY
                name: Right Kidney
                tools:
                  - CHAIN
    """)
    script.sync_configuration(configuration)

    # Update configuration
    configuration = yaml.load("""
        datasets:
          - key: KIDNEYS
            name: New Kidneys
            tasks:
              - KIDNEYS_SEGMENTATION

        tasks:
          - key: KIDNEYS_SEGMENTATION
            name: New Kidneys segmentation
            image_path: new_assets/icon/kidneys_dataset_icon.svg
            tags:
              - key: LEFT_KIDNEY
                name: New Left Kidney
                tools:
                  - CHAIN
                  - BRUSH
              - key: RIGHT_KIDNEY
                name: New Right Kidney
                tools:
                  - CHAIN
    """)
    script.sync_configuration(configuration)

    # Check if Datasets were synchronized properly
    datasets = DatasetsRepository.get_all_datasets(include_disabled=True)
    assert len(datasets) == 1
    kidneys = DatasetsRepository.get_dataset_by_key('KIDNEYS')
    assert kidneys.name == 'New Kidneys'
    assert not kidneys.disabled
    assert {task.key for task in kidneys.tasks} == {'KIDNEYS_SEGMENTATION'}

    # Check if Tasks were synchronized properly
    tasks = TasksRepository.get_all_tasks(include_disabled=True)
    assert len(tasks) == 1
    kidneys_segmentation = TasksRepository.get_task_by_key('KIDNEYS_SEGMENTATION')
    assert kidneys_segmentation.name == 'New Kidneys segmentation'
    assert kidneys_segmentation.image_path == 'new_assets/icon/kidneys_dataset_icon.svg'
    assert not kidneys_segmentation.disabled
    assert len(kidneys_segmentation.available_tags) == 2
    assert {tag.key for tag in kidneys_segmentation.available_tags} == {'LEFT_KIDNEY', 'RIGHT_KIDNEY'}

    # Check if Label Tags were synchronized properly
    tags = LabelTagsRepository.get_all_tags(include_disabled=True)
    assert len(tags) == 2
    left_kidney = LabelTagsRepository.get_label_tag_by_key('LEFT_KIDNEY')
    assert left_kidney.name == 'New Left Kidney'
    assert not left_kidney.disabled
    assert {tool.name for tool in left_kidney.tools} == {'CHAIN', 'BRUSH'}
    right_kidney = LabelTagsRepository.get_label_tag_by_key('RIGHT_KIDNEY')
    assert right_kidney.name == 'New Right Kidney'
    assert not right_kidney.disabled
    assert {tool.name for tool in right_kidney.tools} == {'CHAIN'}


def test_sync_with_changed_tools_in_tag(prepare_environment: Any) -> None:
    """Test for adding and removing Tools in given Label Tag."""
    configuration = yaml.load("""
        datasets:
          - key: KIDNEYS
            name: Kidneys
            tasks:
              - KIDNEYS_SEGMENTATION

        tasks:
          - key: KIDNEYS_SEGMENTATION
            name: Kidneys segmentation
            image_path: assets/icon/kidneys_dataset_icon.svg
            tags:
              - key: LEFT_KIDNEY
                name: Left Kidney
                tools:
                  - CHAIN
                  - BRUSH
    """)
    script.sync_configuration(configuration)

    # Check if Tags were properly synchronized
    tags = LabelTagsRepository.get_all_tags(include_disabled=True)
    assert len(tags) == 1
    left_kidney = LabelTagsRepository.get_label_tag_by_key('LEFT_KIDNEY')
    assert left_kidney.name == 'Left Kidney'
    assert not left_kidney.disabled
    assert {tool.name for tool in left_kidney.tools} == {'CHAIN', 'BRUSH'}

    # Now, let's change Tools for Kidneys Segmentation
    configuration = yaml.load("""
        datasets:
          - key: KIDNEYS
            name: Kidneys
            tasks:
              - KIDNEYS_SEGMENTATION

        tasks:
          - key: KIDNEYS_SEGMENTATION
            name: Kidneys segmentation
            image_path: assets/icon/kidneys_dataset_icon.svg
            tags:
              - key: LEFT_KIDNEY
                name: Left Kidney
                tools:
                  - BRUSH
                  - RECTANGLE
    """)
    script.sync_configuration(configuration)

    # Check if Tags were properly synchronized
    tags = LabelTagsRepository.get_all_tags(include_disabled=True)
    assert len(tags) == 1
    left_kidney = LabelTagsRepository.get_label_tag_by_key('LEFT_KIDNEY')
    assert left_kidney.name == 'Left Kidney'
    assert not left_kidney.disabled
    assert {tool.name for tool in left_kidney.tools} == {'BRUSH', 'RECTANGLE'}


def test_sync_with_changed_tags_in_task(prepare_environment: Any) -> None:
    """Test for adding and removing Tags in Task."""
    configuration = yaml.load("""
        datasets:
          - key: KIDNEYS
            name: Kidneys
            tasks:
              - KIDNEYS_SEGMENTATION

        tasks:
          - key: KIDNEYS_SEGMENTATION
            name: Kidneys segmentation
            image_path: assets/icon/kidneys_dataset_icon.svg
            tags:
              - key: LEFT_KIDNEY
                name: Left Kidney
                tools:
                  - CHAIN
                  - BRUSH
    """)
    script.sync_configuration(configuration)

    # Check if Label Tags were properly synchronized
    tags = LabelTagsRepository.get_all_tags(include_disabled=True)
    assert len(tags) == 1
    left_kidney = LabelTagsRepository.get_label_tag_by_key('LEFT_KIDNEY')
    assert left_kidney.name == 'Left Kidney'
    assert not left_kidney.disabled
    assert {tool.name for tool in left_kidney.tools} == {'CHAIN', 'BRUSH'}

    # Now, let's change Tags for Kidneys Segmentation
    configuration = yaml.load("""
        datasets:
          - key: KIDNEYS
            name: Kidneys
            tasks:
              - KIDNEYS_SEGMENTATION

        tasks:
          - key: KIDNEYS_SEGMENTATION
            name: Kidneys segmentation
            image_path: assets/icon/kidneys_dataset_icon.svg
            tags:
              - key: RIGHT_KIDNEY
                name: Right Kidney
                tools:
                  - RECTANGLE
    """)
    script.sync_configuration(configuration)

    # Check if Tasks were properly synchronized
    tags = LabelTagsRepository.get_all_tags(include_disabled=True)
    assert len(tags) == 2
    left_kidney = LabelTagsRepository.get_label_tag_by_key('LEFT_KIDNEY')
    assert left_kidney.name == 'Left Kidney'
    assert left_kidney.disabled
    assert {tool.name for tool in left_kidney.tools} == {'CHAIN', 'BRUSH'}
    right_kidney = LabelTagsRepository.get_label_tag_by_key('RIGHT_KIDNEY')
    assert right_kidney.name == 'Right Kidney'
    assert not right_kidney.disabled
    assert {tool.name for tool in right_kidney.tools} == {'RECTANGLE'}


def test_sync_with_changed_task_in_dataset(mocker: Any, prepare_environment: Any) -> None:
    """Test for adding and removing Task in DataSet."""
    configuration = yaml.load("""
        datasets:
          - key: KIDNEYS
            name: Kidneys
            tasks:
              - KIDNEYS_SEGMENTATION

        tasks:
          - key: KIDNEYS_SEGMENTATION
            name: Kidneys segmentation
            image_path: assets/icon/kidneys_dataset_icon.svg
            tags:
              - key: LEFT_KIDNEY
                name: Left Kidney
                tools:
                  - CHAIN
                  - BRUSH
    """)
    script.sync_configuration(configuration)

    # Check if Datasets were synchronized properly
    datasets = DatasetsRepository.get_all_datasets(include_disabled=True)
    assert len(datasets) == 1

    # Check if Tasks were synchronized properly
    tasks = TasksRepository.get_all_tasks(include_disabled=True)
    assert len(tasks) == 1
    kidneys_segmentation = TasksRepository.get_task_by_key('KIDNEYS_SEGMENTATION')
    assert kidneys_segmentation.name == 'Kidneys segmentation'
    assert not kidneys_segmentation.disabled

    # Now, let's change Tasks for Kidneys
    configuration = yaml.load("""
        datasets:
          - key: KIDNEYS
            name: Kidneys
            tasks:
             - KIDNEYS_SEGMENTATION

        tasks:
          - key: FIND_NODULES
            name: Find nodules
            image_path: assets/icon/kidneys_dataset_icon.svg
            tags:
              - key: NODULE
                name: Nodule
                tools:
                  - BRUSH
    """)
    script.sync_configuration(configuration)

    # Check if Datasets were synchronized properly
    datasets = DatasetsRepository.get_all_datasets(include_disabled=True)
    assert len(datasets) == 1

    # Check if Tasks were synchronized properly
    tasks = TasksRepository.get_all_tasks(include_disabled=True)
    assert len(tasks) == 2
    kidneys_segmentation = TasksRepository.get_task_by_key('KIDNEYS_SEGMENTATION')
    assert kidneys_segmentation.name == 'Kidneys segmentation'
    assert kidneys_segmentation.disabled
    find_nodules = TasksRepository.get_task_by_key('FIND_NODULES')
    assert find_nodules.name == 'Find nodules'
    assert not find_nodules.disabled

    # Now, let's change let's get back to older Tasks (with different values) for Kidneys
    configuration = yaml.load("""
        datasets:
          - key: KIDNEYS
            name: Kidneys
            tasks:
             - KIDNEYS_SEGMENTATION

        tasks:
          - key: KIDNEYS_SEGMENTATION
            name: New Kidneys segmentation
            image_path: assets/icon/kidneys_dataset_icon.svg
            tags:
              - key: NEW_LEFT_KIDNEY
                name: New Left Kidney
                tools:
                  - RECTANGLE
    """)
    script.sync_configuration(configuration)

    # Check if Datasets were synchronized properly
    datasets = DatasetsRepository.get_all_datasets(include_disabled=True)
    assert len(datasets) == 1

    # Check if Tasks were synchronized properly
    tasks = TasksRepository.get_all_tasks(include_disabled=True)
    assert len(tasks) == 2
    find_nodules = TasksRepository.get_task_by_key('FIND_NODULES')
    assert find_nodules.name == 'Find nodules'
    assert find_nodules.disabled
    kidneys_segmentation = TasksRepository.get_task_by_key('KIDNEYS_SEGMENTATION')
    assert kidneys_segmentation.name == 'New Kidneys segmentation'
    assert kidneys_segmentation.image_path == 'assets/icon/kidneys_dataset_icon.svg'
    assert not kidneys_segmentation.disabled
    assert len(kidneys_segmentation.available_tags) == 1
    assert {tag.key for tag in kidneys_segmentation.available_tags} == {'NEW_LEFT_KIDNEY'}

    # Check if Label Tags were synchronized properly
    tags = LabelTagsRepository.get_all_tags(include_disabled=True)
    assert len(tags) == 3
    left_kidney = LabelTagsRepository.get_label_tag_by_key('LEFT_KIDNEY')
    assert left_kidney.disabled
    nodule = LabelTagsRepository.get_label_tag_by_key('NODULE')
    assert nodule.disabled
    new_left_kidney = LabelTagsRepository.get_label_tag_by_key('NEW_LEFT_KIDNEY')
    assert not new_left_kidney.disabled

    # Now, let's change let's get back to the original Tasks for Kidneys
    mocked_logger = mocker.patch.object(script, 'logger')
    configuration = yaml.load("""
        datasets:
          - key: KIDNEYS
            name: Kidneys
            tasks:
             - KIDNEYS_SEGMENTATION

        tasks:
          - key: KIDNEYS_SEGMENTATION
            name: Kidneys segmentation
            image_path: assets/icon/kidneys_dataset_icon.svg
            tags:
              - key: LEFT_KIDNEY
                name: Left Kidney
                tools:
                  - CHAIN
                  - BRUSH
    """)
    script.sync_configuration(configuration)

    # Check if user was warned about possible data inconsistency
    mocked_logger.warning.assert_called_once_with(
        'Reusing previously existing Label Tag (%s)! This may cause data inconsistency! '
        'Make sure you know what you are doing and clear database entries if necessary!',
        'LEFT_KIDNEY',
    )

    # Check if Label Tags were synchronized properly
    tags = LabelTagsRepository.get_all_tags(include_disabled=True)
    assert len(tags) == 3
    left_kidney = LabelTagsRepository.get_label_tag_by_key('LEFT_KIDNEY')
    assert not left_kidney.disabled
    nodule = LabelTagsRepository.get_label_tag_by_key('NODULE')
    assert nodule.disabled
    new_left_kidney = LabelTagsRepository.get_label_tag_by_key('NEW_LEFT_KIDNEY')
    assert new_left_kidney.disabled


def test_sync_with_changed_dataset_and_reused_task(prepare_environment: Any) -> None:
    """Test for changing DataSet and reusing Task."""
    configuration = yaml.load("""
        datasets:
          - key: KIDNEYS
            name: Kidneys
            tasks:
              - FIND_NODULES

        tasks:
          - key: FIND_NODULES
            name: Find nodules
            image_path: assets/icon/kidneys_dataset_icon.svg
            tags:
              - key: NODULE
                name: Nodule
                tools:
                  - BRUSH
    """)
    script.sync_configuration(configuration)

    # Check if Datasets were synchronized properly
    datasets = DatasetsRepository.get_all_datasets(include_disabled=True)
    assert len(datasets) == 1
    kidneys = DatasetsRepository.get_dataset_by_key('KIDNEYS')
    assert kidneys.name == 'Kidneys'
    assert not kidneys.disabled
    assert {task.key for task in kidneys.tasks} == {'FIND_NODULES'}

    # Now, let's change Tools for Kidneys Segmentation
    configuration = yaml.load("""
        datasets:
          - key: LUNGS
            name: Lungs
            tasks:
              - FIND_NODULES

        tasks:
          - key: FIND_NODULES
            name: Find nodules
            image_path: assets/icon/kidneys_dataset_icon.svg
            tags:
              - key: NODULE
                name: Nodule
                tools:
                  - BRUSH
    """)
    script.sync_configuration(configuration)

    # Check if Datasets were synchronized properly
    datasets = DatasetsRepository.get_all_datasets(include_disabled=True)
    assert len(datasets) == 2
    kidneys = DatasetsRepository.get_dataset_by_key('KIDNEYS')
    assert kidneys.name == 'Kidneys'
    assert kidneys.disabled
    assert {task.key for task in kidneys.tasks} == set()
    lungs = DatasetsRepository.get_dataset_by_key('LUNGS')
    assert lungs.name == 'Lungs'
    assert not lungs.disabled
    assert {task.key for task in lungs.tasks} == {'FIND_NODULES'}
