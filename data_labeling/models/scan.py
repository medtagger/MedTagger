"""Module responsible for definition of Scan model"""
import uuid
from typing import List, Iterable, Any, cast

from data_labeling.models.slice import Slice
from data_labeling.types import ScanID, SliceID, SlicePosition, SliceLocation
from data_labeling.clients.hbase_client import HBaseClient
from data_labeling.workers.storage import store_dicom
from data_labeling.workers.conversion import convert_dicom_to_png


class Scan(object):
    """Definition of a Scan"""

    def __init__(self, scan_id: ScanID = None) -> None:
        """Initializer

        :param scan_id: ID of a Scan that can be used to fetch existing scan from HBase
        """
        self.id = scan_id if scan_id else ScanID(str(uuid.uuid4()))
        self.hbase_client = HBaseClient()

    def create_if_needed(self) -> None:
        """Add new entry in Scans table if scan doesn't exist"""
        if not self._exists:
            initial_data = {
                'metadata:owner': ''
            }
            self.hbase_client.put(HBaseClient.SCANS, self.id, initial_data)

    @property
    def slices(self) -> Iterable[Slice]:
        """Fetch all slices from Slices table related with this Scan

        TODO: This method may be slow in the future! Let's try to move Scans to SQL DB or find faster way to
              get information about Slices for given Scan.

        :return: generator of Slices
        """
        print('Looking for slices for:', self.id)
        slices_from_hbase = self.hbase_client.get_all_rows(HBaseClient.ORIGINAL_SLICES_TABLE, columns=['position'],
                                                           starts_with=self.id)
        for slice_id, data in slices_from_hbase:
            slice_id = SliceID(slice_id)
            location = SliceLocation(float(data[b'position:location'].decode('utf-8')))
            position = SlicePosition(x=float(data[b'position:x'].decode('utf-8')),
                                     y=float(data[b'position:y'].decode('utf-8')),
                                     z=float(data[b'position:z'].decode('utf-8')))
            yield Slice(slice_id, location=location, position=position)

    @property
    def slices_keys(self) -> List[SliceID]:
        """Fetch all keys from Slices table related with this Scan

        TODO: This method may be slow in the future! Let's try to move Scans to SQL DB or find faster way to
              get information about Slices for given Scan.

        :return: list of Slice IDs (keys in HBase)
        """
        keys = self.hbase_client.get_all_keys(HBaseClient.ORIGINAL_SLICES_TABLE, starts_with=self.id)
        return cast(List[SliceID], list(keys))

    def add_slice(self, dicom_image_file: Any) -> None:
        """Add new slice to this Scan and convert it to png format

        This method will trigger Celery task that will add given Dicom to HBase asynchronously, then another Celery
        task will be triggered that will convert Dicom to png format and save it to HBase asynchronously.

        :param dicom_image_file: Dicom file with slice data
        """
        slice_id = str(uuid.uuid4())
        store_dicom.delay(self.id, slice_id, dicom_image_file)
        convert_dicom_to_png.delay(self.id, slice_id, dicom_image_file)

    @property
    def _exists(self) -> bool:
        """Check if given Scan exists in HBase

        :return: boolean information if such Scan exists or not
        """
        return self.hbase_client.check_if_exists(HBaseClient.SCANS, key=self.id)
