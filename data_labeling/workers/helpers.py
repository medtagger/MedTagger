"""Module for storage and conversion helpers functions"""
from typing import Tuple, Dict

from dicom.dataset import FileDataset

from data_labeling.types import ScanID, SliceID


def prepare_hbase_slice_entry(scan_id: ScanID, slice_id: SliceID, dicom_image: FileDataset) -> Tuple[str, Dict]:
    """Preparing slice entry for HBase

    :param scan_id: ID of a scan that contains given slice
    :param slice_id: ID of a slice
    :param dicom_image: Dicom object
    :return: Tuple of slice key and slice positions
    """
    slice_key = str(scan_id) + '__' + str(slice_id)
    slice_value = {
        'position:x': str(dicom_image.ImagePositionPatient[0]),
        'position:y': str(dicom_image.ImagePositionPatient[1]),
        'position:z': str(dicom_image.ImagePositionPatient[2]),
        'position:location': str(dicom_image.SliceLocation),
    }
    return slice_key, slice_value
