"""Module responsible for definition of Labels' Repository."""
from sqlalchemy.sql.expression import func

from medtagger.clients.hbase_client import HBaseClient
from medtagger.database import db_session
from medtagger.database.models import Label, LabelStatus, LabelSelection
from medtagger.types import LabelID, LabelPosition, LabelShape, LabelBinaryMask, LabelSelectionID, ScanID


class LabelsRepository(object):
    """Repository for Labels."""

    @staticmethod
    def get_label_by_id(label_id: LabelID) -> Label:
        """Fetch Label from database."""
        with db_session() as session:
            label = session.query(Label).filter(Label.id == label_id).one()
        return label

    @staticmethod
    def get_random_label(status: LabelStatus = None) -> Label:
        """Fetch random Label from database.

        :param status: (optional) status for Label
        :return: Label object
        """
        with db_session() as session:
            query = session.query(Label)
            if status:
                query = query.filter(Label.status == status)
            query = query.order_by(func.random())
            label = query.first()
        return label

    @staticmethod
    def add_new_label(scan_id: ScanID) -> Label:
        """Add new Label for given Scan."""
        with db_session() as session:
            label = Label()
            label.scan_id = scan_id
            session.add(label)
        return label

    @staticmethod
    def add_new_label_selection(label_id: LabelID, position: LabelPosition, shape: LabelShape,
                                binary_mask: LabelBinaryMask = None) -> LabelSelectionID:
        """Add new Selection for given Label.

        :param label_id: Label's ID
        :param position: position (x, y, slice_index) of the Label
        :param shape: shape (width, height, depth) of the Label
        :param binary_mask: binary mask of the new Selection
        :return: ID of a Selection
        """
        with db_session() as session:
            new_label_selection = LabelSelection(position, shape)
            new_label_selection.label_id = label_id
            session.add(new_label_selection)

        if binary_mask:
            LabelsRepository._store_labels_selection_binary_mask(new_label_selection.id, binary_mask)

        return new_label_selection.id

    @staticmethod
    def _store_labels_selection_binary_mask(label_selection_id: LabelSelectionID, binary_mask: bytes) -> None:
        """Store Label's Selection binary mask into HBase."""
        binary_mask_value = {
            'binary_mask:value': binary_mask,
        }
        hbase_client = HBaseClient()
        hbase_client.put(HBaseClient.LABEL_SELECTION_BINARY_MASK_TABLE, label_selection_id, binary_mask_value)
