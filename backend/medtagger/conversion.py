"""Module responsible for conversion of Dicom files."""
from typing import List, Any, Optional

import numpy as np
import SimpleITK as sitk
from scipy import ndimage

from medtagger.definitions import DicomTags


def convert_slice_to_normalized_8bit_array(dicom_file: sitk.Image) -> np.ndarray:
    """Convert Dicom file to 8bit pixel array.

    :param: dicom_file: Dicom file that will be converted to a pixel array
    :return numpy array of pixels
    """
    pixel_array = sitk.GetArrayFromImage(dicom_file)[0]
    intercept = float(dicom_file.GetMetaData(DicomTags.RESCALE_INTERCEPT.value))
    slope = float(dicom_file.GetMetaData(DicomTags.RESCALE_SLOPE.value))

    try:
        rescale_type = dicom_file.GetMetaData(DicomTags.RESCALE_TYPE.value)
    except RuntimeError:
        rescale_type = None

    if rescale_type not in {'normalized', 'US'}:
        hu_units_array = convert_to_hounsfield_units(pixel_array, intercept, slope)
        normalized_hu_array = normalize(hu_units_array)
        pixel_array = normalized_hu_array

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
    dicom_files = sorted(dicom_files, key=lambda _slice: float(_slice.GetMetaData(DicomTags.SLICE_LOCATION.value)),
                         reverse=True)
    thickness = _get_scan_slice_thickness(dicom_files)
    spacing = float(dicom_files[0].GetMetaData(DicomTags.PIXEL_SPACING.value).split('\\')[0])
    intercept = float(dicom_files[0].GetMetaData(DicomTags.RESCALE_INTERCEPT.value))
    slope = float(dicom_files[0].GetMetaData(DicomTags.RESCALE_SLOPE.value))

    # Read all Dicom images and retrieve pixel values for each slice
    pixel_array = np.array(np.stack(sitk.GetArrayFromImage(_slice)[0] for _slice in dicom_files))

    # Calculate scale factor that should be applied to the input 3D scan
    real_shape = np.array([thickness, spacing, spacing]) * pixel_array.shape  # Shape after applying voxel's size
    # `scale` tell us how much should we rescale real shape, so that X axis will be equal given size
    scale = output_x_size / real_shape[2] if output_x_size else 1.0
    after_rescale = real_shape * scale  # Shape which should be an output after the scaling
    scale_factor = after_rescale / pixel_array.shape  # Calculate how much each of the axis should be scaled up/down
    pixel_array = ndimage.zoom(pixel_array, scale_factor)  # Scale all images up/down

    try:
        rescale_type = dicom_files[0].GetMetaData(DicomTags.RESCALE_TYPE.value)
    except RuntimeError:
        rescale_type = None

    if rescale_type not in {'normalized', 'US'}:
        hu_units_array = convert_to_hounsfield_units(pixel_array, intercept, slope)
        normalized_hu_array = normalize(hu_units_array)
        pixel_array = normalized_hu_array

    pixel_array_normalized = (pixel_array - np.min(pixel_array)) / (np.max(pixel_array) - np.min(pixel_array))
    pixel_array = np.uint8(pixel_array_normalized * 255)
    return pixel_array


def convert_to_hounsfield_units(pixel_array: np.ndarray, intercept: float, slope: float) -> np.ndarray:
    """Convert given Slice's pixel array to Hounsfield units.

    :param pixel_array: Slice's pixel array (taken from Dicom file)
    :param intercept: intercept for linear function taken from Dicom file
    :param slope: slope for linear function taken from Dicom file
    :return: numpy array with Slice's pixel array
    """
    # Set outside-of-scan pixels to 0
    pixel_array[pixel_array == -2000] = 0

    # If slope equals 1 the instructions below would be unnecessary
    if slope != 1:
        pixel_array = slope * pixel_array
        pixel_array = pixel_array

    pixel_array = pixel_array + intercept
    return pixel_array


def normalize(hu_array: np.ndarray, min_bound: int = -360, max_bound: int = 440) -> np.ndarray:
    """Normalize values of the Hounsfield units array.

    :param hu_array: numpy array of Hounsfield units for the Dicom file
    :param min_bound: minimal Hounsfield units value
    :param max_bound: maximum Hounsfield units value
    :return: normalized-numpy-two-dimensional array of Hounsfield units
    """
    hu_array = (hu_array - min_bound) / (max_bound - min_bound)
    hu_array[hu_array > 1] = 1.
    hu_array[hu_array < 0] = 0.
    return hu_array


def _get_scan_slice_thickness(dicom_files: List[Any]) -> float:
    """Calculate Scan's Slice thickness.

    :param dicom_files: list of all Dicom files related to given Scan
    :return: float value with Scan's Slice thickness
    """
    try:
        first_location = float(dicom_files[0].GetMetaData(DicomTags.SLICE_LOCATION.value))
        second_location = float(dicom_files[1].GetMetaData(DicomTags.SLICE_LOCATION.value))
        return abs(second_location - first_location)
    except IndexError:
        return 1.0  # It seems that there is only one Slice. Thickness >=1.0 will be fine for all of the computations.
