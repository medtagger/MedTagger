"""Module responsible for business logic in all Datasets endpoints."""
from typing import List

from medtagger.database.models import Dataset
from medtagger.repositories import (
    datasets as DatasetsRepository,
)


def get_available_datasets() -> List[Dataset]:
    """Fetch list of all available Datasets.

    :return: list of Datasets
    """
    return DatasetsRepository.get_all_datasets()


def create_dataset(key: str, name: str) -> Dataset:
    """Create new Dataset.

    :param key: unique key representing Dataset
    :param name: name which describes this Dataset
    :return: Dataset object
    """
    return DatasetsRepository.add_new_dataset(key, name)
