"""Definition of storage for MedTagger."""
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.columns import Text, Blob

from medtagger.storage import models

MEDTAGGER_KEYSPACE = 'medtagger'


class CassandraOriginalSlice(Model):
    """Model representing original Slice image."""

    __table_name__ = 'original_slices'
    __keyspace__ = MEDTAGGER_KEYSPACE

    id = Text(primary_key=True)
    image = Blob()

    def as_unified_model(self) -> models.OriginalSlice:
        return models.OriginalSlice(id=self.id, image=self.image)


class CassandraProcessedSlice(Model):
    """Model representing processed Slice image."""

    __table_name__ = 'processed_slices'
    __keyspace__ = MEDTAGGER_KEYSPACE

    id = Text(primary_key=True)
    image = Blob()

    def as_unified_model(self) -> models.ProcessedSlice:
        return models.ProcessedSlice(id=self.id, image=self.image)


class CassandraBrushLabelElement(Model):
    """Model representing Label Element made with Brush Tool."""

    __table_name__ = 'brush_label_elements'
    __keyspace__ = MEDTAGGER_KEYSPACE

    id = Text(primary_key=True)
    image = Blob()

    def as_unified_model(self) -> models.BrushLabelElement:
        return models.BrushLabelElement(id=self.id, image=self.image)
