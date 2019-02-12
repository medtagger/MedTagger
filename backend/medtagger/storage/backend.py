import abc


class StorageBackend(abc.ABC):

    def is_alive(self) -> bool:
        raise NotImplementedError('This method is not implemented!')

    def get(self, model: type, **filters):
        raise NotImplementedError('This method is not implemented!')

    def create(self, model: type, **data):
        raise NotImplementedError('This method is not implemented!')

    def delete(self, model: type, **filters) -> None:
        raise NotImplementedError('This method is not implemented!')
