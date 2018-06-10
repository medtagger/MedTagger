"""Definition of storage for MedTagger."""
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.columns import Text, Blob

from medtagger.storage import MEDTAGGER_KEYSPACE


class OriginalSlice(Model):
    """Model representing original Slice image."""

    __table_name__ = 'original_slices'
    __keyspace__ = MEDTAGGER_KEYSPACE

    id = Text(primary_key=True)
    image = Blob()


class ProcessedSlice(Model):
    """Model representing processed Slice image."""

    __table_name__ = 'processed_slices'
    __keyspace__ = MEDTAGGER_KEYSPACE

    id = Text(primary_key=True)
    image = Blob()


class BrushLabelElement(Model):
    """Model representing Label Element made with Brush Tool."""

    __table_name__ = 'brush_label_elements'
    __keyspace__ = MEDTAGGER_KEYSPACE

    id = Text(primary_key=True)
    image = Blob()
