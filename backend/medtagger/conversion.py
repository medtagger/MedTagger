"""Module responsible for conversion of Dicom files."""
from typing import List, Optional

import numpy as np
from scipy import ndimage
from dicom.dataset import FileDataset


def convert_slice_to_normalized_8bit_array(dicom_file: FileDataset) -> np.ndarray:
    """Convert Dicom file to 8bit pixel array.

    :param: dicom_file: Dicom file that will be converted to a pixel array
    :return numpy array of pixels
    """
    pixel_array = dicom_file.pixel_array
    intercept = dicom_file.RescaleIntercept
    slope = dicom_file.RescaleSlope

    hu_units_array = convert_to_hounsfield_units(pixel_array, intercept, slope)
    normalized_hu_array = normalize(hu_units_array)

    pixel_array = normalized_hu_array * 255
    pixel_array = pixel_array.astype(np.int8)
    return pixel_array


def convert_scan_to_normalized_8bit_array(dicom_files: List[FileDataset], output_x_size: Optional[int] = None) \
        -> np.ndarray:
    """Convert list of Dicom files to 8bit pixel array with output X axis size.

    :param dicom_files: list of Dicom files related with given Scan
    :param output_x_size: (optional) X axis size for output shape
    :return: 3D numpy array with normalized pixels
    """
    dicom_files = sorted(dicom_files, key=lambda _slice: _slice.SliceLocation, reverse=True)
    thickness = _get_scan_slice_thickness(dicom_files)
    spacing = float(dicom_files[0].PixelSpacing.pop())
    intercept = dicom_files[0].RescaleIntercept
    slope = dicom_files[0].RescaleSlope

    # Read all Dicom images and retrieve pixel values for each slice
    pixel_array = np.array(np.stack(_slice.pixel_array for _slice in dicom_files))

    # Calculate scale factor that should be applied to the input 3D scan
    real_shape = np.array([thickness, spacing, spacing]) * pixel_array.shape  # Shape after applying voxel's size
    # `scale` tell us how much should we rescale real shape, so that X axis will be equal given size
    scale = output_x_size / real_shape[2] if output_x_size else 1.0
    after_rescale = real_shape * scale  # Shape which should be an output after the scaling
    scale_factor = after_rescale / pixel_array.shape  # Calculate how much each of the axis should be scaled up/down
    pixel_array = ndimage.zoom(pixel_array, scale_factor)  # Scale all images up/down

    hu_units_array = convert_to_hounsfield_units(pixel_array, intercept, slope)
    normalized_hu_array = normalize(hu_units_array)

    pixel_array = normalized_hu_array * 255
    pixel_array = pixel_array.astype(np.int8)
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


def _get_scan_slice_thickness(dicom_files: List[FileDataset]) -> float:
    """Calculate Scan's Slice thickness.

    :param dicom_files: list of all Dicom files related to given Scan
    :return: float value with Scan's Slice thickness
    """
    try:
        return abs(dicom_files[0].SliceLocation - dicom_files[1].SliceLocation)
    except IndexError:
        return 1.0  # It seems that there is only one Slice. Thickness >=1.0 will be fine for all of the computations.
