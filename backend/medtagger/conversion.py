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

    hu_units_array = get_hu_units(pixel_array, intercept, slope)
    normalized_hu_array = normalize(hu_units_array)

    pixel_array = normalized_hu_array * 255
    pixel_array = pixel_array.astype(np.int8)
    return pixel_array


def convert_scan_to_normalized_8bit_array(dicom_files: List[FileDataset], output_x_size: Optional[int] = None) \
        -> np.ndarray:
    """Convert list of Dicom files to 8bit pixel array with output X axis size.

    :param dicom_files:
    :param output_x_size:
    :return:
    """
    dicom_files = sorted(dicom_files, key=lambda _slice: _slice.SliceLocation, reverse=True)
    thickness = abs(dicom_files[0].SliceLocation - dicom_files[1].SliceLocation)
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

    hu_units_array = get_hu_units(pixel_array, intercept, slope)
    normalized_hu_array = normalize(hu_units_array)

    pixel_array = normalized_hu_array * 255
    pixel_array = pixel_array.astype(np.int8)
    return pixel_array


def get_hu_units(dicom_pixel_array: np.ndarray, intercept: float, slope: float) -> np.ndarray:
    """Extract HU (Hounsfield units) from Dicom file.

    :param dicom_pixel_array:
    :param intercept:
    :param slope:
    :return:
    """
    # Set outside-of-scan pixels to 0
    dicom_pixel_array[dicom_pixel_array == -2000] = 0

    # If slope equals 1 the instructions below would be unnecessary
    if slope != 1:
        dicom_pixel_array = slope * dicom_pixel_array.astype(np.float64)  # pylint: disable=no-member; bug
        dicom_pixel_array = dicom_pixel_array.astype(np.int16)

    dicom_pixel_array += np.int16(intercept)
    return dicom_pixel_array


def normalize(hu_array: np.ndarray, min_bound: int = -1000, max_bound: int = 400) -> np.ndarray:
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
