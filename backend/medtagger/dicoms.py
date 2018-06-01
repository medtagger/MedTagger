"""Helpers for parsing DICOM images."""
from typing import List, Union, Optional

import SimpleITK as sitk

from medtagger.definitions import DicomTag


def read_int(dicom: Union[sitk.Image, sitk.ImageFileReader], tag: DicomTag) -> Optional[int]:
    """Read an integer value from DICOM image.

    :param dicom: either a DICOM image or reader for DICOM image
    :param tag: DICOM Tag which should be read for this image
    :return: integer value for given Tag or default value
    """
    try:
        return int(dicom.GetMetaData(tag.value))
    except RuntimeError:
        return None


def read_float(dicom: Union[sitk.Image, sitk.ImageFileReader], tag: DicomTag) -> Optional[float]:
    """Read a float value from DICOM image.

    :param dicom: either a DICOM image or reader for DICOM image
    :param tag: DICOM Tag which should be read for this image
    :return: float value for given Tag or default value
    """
    try:
        return float(dicom.GetMetaData(tag.value))
    except RuntimeError:
        return None


def read_string(dicom: Union[sitk.Image, sitk.ImageFileReader], tag: DicomTag) -> Optional[str]:
    """Read a string value from DICOM image.

    :param dicom: either a DICOM image or reader for DICOM image
    :param tag: DICOM Tag which should be read for this image
    :return: string value for given Tag or default value
    """
    try:
        return dicom.GetMetaData(tag.value)
    except RuntimeError:
        return None


def read_list(dicom: Union[sitk.Image, sitk.ImageFileReader], tag: DicomTag) -> Optional[List]:
    """Read a list value from DICOM image.

    :param dicom: either a DICOM image or reader for DICOM image
    :param tag: DICOM Tag which should be read for this image
    :return: list value for given Tag or default value
    """
    try:
        return dicom.GetMetaData(tag.value).split('\\')
    except RuntimeError:
        return None
