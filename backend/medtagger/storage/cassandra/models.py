"""Definition of storage for MedTagger."""
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.columns import Text, Blob

from medtagger.storage import models

MEDTAGGER_KEYSPACE = 'medtagger'


class CassandraOriginalSlice(Model, models.InternalStorageModel):
    """Model representing original Slice image."""

    __table_name__ = 'original_slices'
    __keyspace__ = MEDTAGGER_KEYSPACE

    id = Text(primary_key=True)
    image = Blob()

    def as_unified_model(self) -> models.OriginalSlice:
        """Convert internal model representation into unified model."""
        return models.OriginalSlice(_id=self.id, image=self.image)


class CassandraProcessedSlice(Model, models.InternalStorageModel):
    """Model representing processed Slice image."""

    __table_name__ = 'processed_slices'
    __keyspace__ = MEDTAGGER_KEYSPACE

    id = Text(primary_key=True)
    image = Blob()

    def as_unified_model(self) -> models.ProcessedSlice:
        """Convert internal model representation into unified model."""
        return models.ProcessedSlice(_id=self.id, image=self.image)


class CassandraBrushLabelElement(Model, models.InternalStorageModel):
    """Model representing Label Element made with Brush Tool."""

    __table_name__ = 'brush_label_elements'
    __keyspace__ = MEDTAGGER_KEYSPACE

    id = Text(primary_key=True)
    image = Blob()

    def as_unified_model(self) -> models.BrushLabelElement:
        """Convert internal model representation into unified model."""
        return models.BrushLabelElement(_id=self.id, image=self.image)
