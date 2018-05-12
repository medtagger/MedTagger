"""Helpers for parsing DICOM images."""
from typing import List, Union

import SimpleITK as sitk

from medtagger.definitions import DicomTag


def read_int(dicom: Union[sitk.Image, sitk.ImageFileReader], tag: DicomTag, default: int = 0) -> int:
    """Read an integer value from DICOM image.

    :param dicom: either a DICOM image or reader for DICOM image
    :param tag: DICOM Tag which should be read for this image
    :param default: (optional) default value which should be returned if there is no such Tag in the DICOM Image
    :return: integer value for given Tag or default value
    """
    try:
        return int(dicom.GetMetaData(tag.value))
    except RuntimeError:
        return default


def read_float(dicom: Union[sitk.Image, sitk.ImageFileReader], tag: DicomTag, default: float = 0.0) -> float:
    """Read a float value from DICOM image.

    :param dicom: either a DICOM image or reader for DICOM image
    :param tag: DICOM Tag which should be read for this image
    :param default: (optional) default value which should be returned if there is no such Tag in the DICOM Image
    :return: float value for given Tag or default value
    """
    try:
        return float(dicom.GetMetaData(tag.value))
    except RuntimeError:
        return default


def read_list(dicom: Union[sitk.Image, sitk.ImageFileReader], tag: DicomTag, default: List = None) -> List:
    """Read a list value from DICOM image.

    :param dicom: either a DICOM image or reader for DICOM image
    :param tag: DICOM Tag which should be read for this image
    :param default: (optional) default value which should be returned if there is no such Tag in the DICOM Image
    :return: list value for given Tag or default value
    """
    try:
        return dicom.GetMetaData(tag.value).split('\\')
    except RuntimeError:
        return default or []
