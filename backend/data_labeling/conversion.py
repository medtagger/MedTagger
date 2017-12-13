"""Module responsible for conversion of Dicom files"""
import numpy as np
from dicom.dataset import FileDataset


def convert_to_normalized_8bit_array(dicom_file: FileDataset) -> np.ndarray:
    """Convert Dicom file to 8bit pixel array

    :param: dicom_file: Dicom file that will be converted to a pixel array
    :return numpy array of pixels
    """
    hu_units_array = get_hu_units(dicom_file)
    normalized_hu_array = normalize(hu_units_array)

    pixel_array = normalized_hu_array * 255
    pixel_array = pixel_array.astype(np.int8)

    return pixel_array


def get_hu_units(dicom_file: FileDataset) -> np.ndarray:
    """Extract HU (Hounsfield units) from Dicom file

    :param dicom_file: Dicom file with a single slice
    :return: numpy array of Hounsfield units for the Dicom file
    """
    dicom_pixel_array = dicom_file.pixel_array.astype(np.int16)

    # Set outside-of-scan pixels to 0
    dicom_pixel_array[dicom_pixel_array == -2000] = 0

    # Convert to Hounsfield units (HU)
    intercept = dicom_file.RescaleIntercept
    slope = dicom_file.RescaleSlope

    # If slope equals 1 the instructions below would be unnecessary
    if slope != 1:
        dicom_pixel_array = slope * dicom_pixel_array.astype(np.float64)  # pylint: disable=no-member; bug
        dicom_pixel_array = dicom_pixel_array.astype(np.int16)

    dicom_pixel_array += np.int16(intercept)

    return dicom_pixel_array


def normalize(hu_array: np.ndarray, min_bound: int = -1000, max_bound: int = 400) -> np.ndarray:
    """Normalizing values of the Hounsfield units array

    :param hu_array: numpy array of Hounsfield units for the Dicom file
    :param min_bound: minimal Hounsfield units value
    :param max_bound: maximum Hounsfield units value
    :return: normalized-numpy-two-dimensional array of Hounsfield units
    """
    hu_array = (hu_array - min_bound) / (max_bound - min_bound)
    hu_array[hu_array > 1] = 1.
    hu_array[hu_array < 0] = 0.

    return hu_array
