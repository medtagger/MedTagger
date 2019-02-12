import os


class FileSystemModel:

    MODEL_DIRECTORY = None

    @classmethod
    def get(cls, filesystem_directory, **filters):
        with open(cls._get_file_location(filesystem_directory, filters['id']), 'rb') as opened_file:
            return cls.from_file(opened_file)

    @classmethod
    def create(cls, filesystem_directory, **data):
        file_location = cls._get_file_location(filesystem_directory, data['id'])
        file_directory = os.path.dirname(file_location)
        os.makedirs(file_directory, exist_ok=True)
        with open(file_location, 'wb+') as opened_file:
            return cls.to_file(opened_file, **data)

    @classmethod
    def delete(cls, filesystem_directory, **filters):
        os.remove(cls._get_file_location(filesystem_directory, filters['id']))

    @classmethod
    def _get_file_location(cls, directory: str, id: str) -> str:
        return f'{directory}/{cls.MODEL_DIRECTORY}/{id[:4]}/{id}'


class FileSystemOriginalSlice(FileSystemModel):

    MODEL_DIRECTORY = 'original_slice'

    def __init__(self, id: str, image: bytes) -> None:
        self.id = id
        self.image = image

    @classmethod
    def from_file(cls, opened_file):
        id = os.path.basename(opened_file.name)
        image = opened_file.read()
        return cls(id, image)

    @classmethod
    def to_file(cls, opened_file, **data):
        opened_file.write(data['image'])


class FileSystemProcessedSlice(FileSystemModel):

    MODEL_DIRECTORY = 'processed_slice'

    def __init__(self, id: str, image: bytes) -> None:
        self.id = id,
        self.image = image

    @classmethod
    def from_file(cls, opened_file):
        id = os.path.basename(opened_file.name)
        image = opened_file.read()
        return cls(id, image)

    @classmethod
    def to_file(cls, opened_file, **data):
        opened_file.write(data['image'])


class FileSystemBrushLabelElement(FileSystemModel):

    MODEL_DIRECTORY = 'brush_label_element'

    def __init__(self, id: str, image: bytes) -> None:
        self.id = id,
        self.image = image

    @classmethod
    def from_file(cls, opened_file):
        id = os.path.basename(opened_file.name)
        image = opened_file.read()
        return cls(id, image)

    @classmethod
    def to_file(cls, opened_file, **data):
        opened_file.write(data['image'])
