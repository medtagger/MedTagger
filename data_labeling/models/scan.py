"""Module responsible for definition of Scan model"""
import uuid
from typing import List, Any, cast

from data_labeling.types import ScanID, SliceID
from data_labeling.clients.hbase_client import HBaseClient
from data_labeling.workers.storage import store_dicom


class Scan(object):
    """Definition of a Scan"""

    def __init__(self, scan_id: ScanID = None) -> None:
        """Initializer

        :param scan_id: ID of a Scan that can be used to fetch existing scan from HBase
        """
        self.connection = HBaseClient()
        self.scans_table = self.connection.table(HBaseClient.SCANS)
        self.id = scan_id if scan_id else ScanID(str(uuid.uuid4()))
        self._hbase_key = str.encode(self.id)

    def create_if_needed(self) -> None:
        """Add new entry in Scans table if scan doesn't exist"""
        if not self._exists():
            initial_data = {
                'metadata:owner': ''
            }
            self.scans_table.put(self._hbase_key, initial_data)

    def get_list_of_slices_keys(self) -> List[SliceID]:
        """Fetch all keys from Slices table related with this Scan

        TODO: This method may be slow in the future! Let's try to move Scans to SQL DB or find faster way to
              get information about Slices for given Scan.

        :return: list of Slice IDs (keys in HBase)
        """
        keys = self.connection.get_all_keys(HBaseClient.ORIGINAL_SLICES_TABLE, starts_with=self.id)
        return cast(List[SliceID], list(keys))

    def add_slice(self, dicom_image_file: Any) -> None:
        """Add new slice to this Scan

        This method will trigger Celery task that will add given Dicom to HBase asynchronously.

        :param dicom_image_file: Dicom file with slice data
        """
        store_dicom.delay(self.id, dicom_image_file)

    def _exists(self) -> bool:
        """Check if given Scan exists in HBase

        :return: boolean information if such Scan exists or not
        """
        return self.connection.check_if_exists(HBaseClient.SCANS, key=self.id)
