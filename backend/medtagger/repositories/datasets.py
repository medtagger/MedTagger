"""Module responsible for definition of DatasetsRepository."""
from typing import List

from medtagger.database import db_session
from medtagger.database.models import Dataset


def get_all_datasets() -> List[Dataset]:
    """Return list of all Datasets."""
    with db_session() as session:
        datasets = session.query(Dataset).order_by(Dataset.id).all()
    return datasets


def get_dataset_by_key(key: str) -> Dataset:
    """Fetch Dataset from database.

    :param key: key for a Dataset
    :return: Dataset object
    """
    with db_session() as session:
        dataset = session.query(Dataset).filter(Dataset.key == key).one()
    return dataset


def add_new_dataset(key: str, name: str) -> Dataset:
    """Add new Dataset to the database.

    :param key: key that will identify such Dataset
    :param name: name that will be used in the Use Interface for such Dataset
    :return: Dataset object
    """
    with db_session() as session:
        dataset = Dataset(key, name)
        session.add(dataset)
    return dataset
