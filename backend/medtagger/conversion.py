"""Module responsible for conversion of Dicom files."""
from typing import List, Any, Optional

import numpy as np
import SimpleITK as sitk
from scipy import ndimage

from medtagger.definitions import DicomTag
from medtagger.dicoms import read_float


def convert_slice_to_normalized_8bit_array(dicom_file: sitk.Image) -> np.ndarray:
    """Convert Dicom file to 8bit pixel array.

    :param: dicom_file: Dicom file that will be converted to a pixel array
    :return numpy array of pixels
    """
    pixel_array = sitk.GetArrayFromImage(dicom_file)[0]
    pixel_array_normalized = (pixel_array - np.min(pixel_array)) / (np.max(pixel_array) - np.min(pixel_array))
    pixel_array = np.uint8(pixel_array_normalized * 255)
    return pixel_array


def convert_scan_to_normalized_8bit_array(dicom_files: List[sitk.Image], output_x_size: Optional[int] = None) \
        -> np.ndarray:
    """Convert list of Dicom files to 8bit pixel array with output X axis size.

    :param dicom_files: list of Dicom files related with given Scan
    :param output_x_size: (optional) X axis size for output shape
    :return: 3D numpy array with normalized pixels
    """
    dicom_files = sorted(dicom_files, key=lambda _slice: read_float(_slice, DicomTag.SLICE_LOCATION), reverse=True)
    thickness = _get_scan_slice_thickness(dicom_files)
    spacing = float(read_list(dicom_files[0], DicomTag.PIXEL_SPACING)[0])

    # Read all Dicom images and retrieve pixel values for each slice
    pixel_array = np.array(np.stack(sitk.GetArrayFromImage(_slice)[0] for _slice in dicom_files))

    # Calculate scale factor that should be applied to the input 3D scan
    real_shape = np.array([thickness, spacing, spacing]) * pixel_array.shape  # Shape after applying voxel's size
    # `scale` tell us how much should we rescale real shape, so that X axis will be equal given size
    scale = output_x_size / real_shape[2] if output_x_size else 1.0
    after_rescale = real_shape * scale  # Shape which should be an output after the scaling
    scale_factor = after_rescale / pixel_array.shape  # Calculate how much each of the axis should be scaled up/down
    pixel_array = ndimage.zoom(pixel_array, scale_factor)  # Scale all images up/down

    pixel_array_normalized = (pixel_array - np.min(pixel_array)) / (np.max(pixel_array) - np.min(pixel_array))
    pixel_array = np.uint8(pixel_array_normalized * 255)
    return pixel_array


def _get_scan_slice_thickness(dicom_files: List[Any]) -> float:
    """Calculate Scan's Slice thickness.

    :param dicom_files: list of all Dicom files related to given Scan
    :return: float value with Scan's Slice thickness
    """
    try:
        first_location = read_float(dicom_files[0], DicomTag.SLICE_LOCATION, default=0.0)
        second_location = read_float(dicom_files[1], DicomTag.SLICE_LOCATION, default=0.0)
        return abs(second_location - first_location)
    except IndexError:
        return 1.0  # It seems that there is only one Slice. Thickness >=1.0 will be fine for all of the computations.
