"""Module responsible for definition of DatasetsRepository."""
from typing import List

from medtagger.database import db_session
from medtagger.database.models import Dataset
from medtagger.exceptions import InternalErrorException


def get_all_datasets(include_disabled: bool = False) -> List[Dataset]:
    """Return list of all Datasets."""
    query = Dataset.query
    if not include_disabled:
        query = query.filter(~Dataset.disabled)
    return query.order_by(Dataset.key).all()


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


def update(key: str, name: str) -> Dataset:
    """Update Dataset in the database.

    :param key: key that will identify such Dataset
    :param name: new name for given Dataset
    :return: Dataset object
    """
    dataset = get_dataset_by_key(key)
    dataset.name = name
    dataset.save()
    return dataset


def disable(key: str) -> None:
    """Disable existing Dataset."""
    disabling_query = Dataset.query.filter(Dataset.key == key)
    updated = disabling_query.update({'disabled': True}, synchronize_session='fetch')
    if not updated:
        raise InternalErrorException(f'Dataset "{key}" was not disabled due to unknown database error.')


def enable(key: str) -> None:
    """Enable existing Dataset."""
    enabling_query = Dataset.query.filter(Dataset.key == key)
    updated = enabling_query.update({'disabled': False}, synchronize_session='fetch')
    if not updated:
        raise InternalErrorException(f'Dataset "{key}" was not enabled due to unknown database error.')
