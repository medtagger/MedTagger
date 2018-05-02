"""Module responsible for definition of Labels' Repository."""
from typing import List

from sqlalchemy.sql.expression import func

from medtagger.database import db_session
from medtagger.database.models import Label, LabelElement, LabelTag, User, LabelVerificationStatus
from medtagger.types import LabelID, LabelPosition, LabelShape, LabelSelectionBinaryMask, LabelElementID, ScanID, \
    LabelingTime

class LabelsRepository(object):
    """Repository for Labels."""

    @staticmethod
    def get_all_labels() -> List[Label]:
        """Fetch all Labels from database."""
        return Label.query.all()

    @staticmethod
    def get_label_by_id(label_id: LabelID, fetch_binary_masks: bool = False) -> Label:
        """Fetch Label from database."""
        with db_session() as session:
            label = session.query(Label).filter(Label.id == label_id).one()
        if fetch_binary_masks:
            label = LabelsRepository._fetch_label_elements_binary_masks(label)
        return label

    @staticmethod
    def get_random_label(status: LabelVerificationStatus = None, fetch_binary_masks: bool = False) -> Label:
        """Fetch random Label from database.

        :param status: (optional) verification status for Label
        :param fetch_binary_masks: (optional) switch for fetching Label's Elements binary masks
        :return: Label object
        """
        with db_session() as session:
            query = session.query(Label)
            if status:
                query = query.filter(Label.status == status)
            query = query.order_by(func.random())
            label = query.first()
        if label and fetch_binary_masks:
            label = LabelsRepository._fetch_label_elements_binary_masks(label)
        return label

    @staticmethod
    def add_new_label(scan_id: ScanID, user: User, labeling_time: LabelingTime) -> Label:
        """Add new Label for given Scan."""
        with db_session() as session:
            label = Label(user, labeling_time)
            label.scan_id = scan_id
            session.add(label)
        return label

    @staticmethod
    def add_new_label_element(label_id: LabelID, position: LabelPosition, shape: LabelShape, label_tag: LabelTag,
                              binary_mask: LabelSelectionBinaryMask = None) -> LabelElementID:
        """Add new Element for given Label.

        :param label_id: Label's ID
        :param position: position (x, y, slice_index) of the Label
        :param shape: shape (width, height, depth) of the Label
        :param label_tag: Label Tag object
        :param binary_mask: binary mask of the new Element
        :return: ID of a Element
        """
        with db_session() as session:
            new_label_element = LabelElement(position, shape, label_tag, has_binary_mask=bool(binary_mask))
            new_label_element.label_id = label_id
            session.add(new_label_element)

        if binary_mask:
            LabelsRepository._store_label_element_binary_mask(new_label_element.id, binary_mask)

        return new_label_element.id

    @staticmethod
    def _fetch_label_elements_binary_masks(label: Label) -> Label:
        """Fetch and fill given Label's Elements with binary masks."""
        for element in label.elements:
            if element.has_binary_mask:
                element.binary_mask = LabelsRepository._get_label_element_binary_mask(element.id)
        return label

    @staticmethod
    def _get_label_element_binary_mask(label_selection_id: LabelElementID) -> LabelSelectionBinaryMask:
        """Return binary mask for given Label Selection."""
        hbase_client = HBaseClient()
        data = hbase_client.get(HBaseClient.LABEL_SELECTION_BINARY_MASK_TABLE, label_selection_id,
                                columns=['binary_mask'])
        return LabelSelectionBinaryMask(data[b'binary_mask:value'].decode('utf-8'))

    @staticmethod
    def _store_label_element_binary_mask(label_element_id: LabelElementID,
                                         binary_mask: LabelSelectionBinaryMask) -> None:
        """Store Label's Element binary mask into HBase.

        :param label_element_id: Label Element's ID
        :param binary_mask: binary mask of the new Selection
        """
        binary_mask_value = {
            'binary_mask:value': binary_mask,
        }
        hbase_client = HBaseClient()
        hbase_client.put(HBaseClient.LABEL_SELECTION_BINARY_MASK_TABLE, label_element_id, binary_mask_value)
