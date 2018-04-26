"""Script that will convert multiple dicoms to PNG format.

How to use it?
--------------
At first, download some scans from anywhere on the Internet. You can use example dataset from Data Science Bowl 2017:
https://www.kaggle.com/c/data-science-bowl-2017/data (look for 'sample_images.7z' file).

Then, place these data (unzipped) anywhere on your computer and run this script by:

    (venv) $ python3.6 scripts/dicoms_to_png.py --input=./dir_with_scans/ --output=./dir_with_scans/converted/

Name of the converted Dicom file is a position of the scan on the z axis.
"""
import os
import argparse

import SimpleITK as sitk
from PIL import Image

from medtagger.definitions import DicomTags
from medtagger.conversion import convert_slice_to_normalized_8bit_array


parser = argparse.ArgumentParser(description='Convert dicoms to png format.')
parser.add_argument('--input', type=str, required=True, help='Full path to directory where dicoms are located')
parser.add_argument('--output', type=str, required=True,
                    help='Full path to directory where converted dicoms would be located')

args = parser.parse_args()
dicoms_folder_path = args.input
converted_dicoms_folder_path = args.output

dicoms = [sitk.ReadImage(dicoms_folder_path + d) for d in os.listdir(dicoms_folder_path) if
          os.path.isfile(dicoms_folder_path + d)]
min_position = abs(min([dicom.GetMetaData(DicomTags.IMAGE_POSITION_PATIENT.value).split('\\')[2] for dicom in dicoms]))

if not os.path.exists(converted_dicoms_folder_path):
    os.mkdir(converted_dicoms_folder_path)

for single_dicom in dicoms:
    image_bytes = convert_slice_to_normalized_8bit_array(single_dicom)
    slice_position = single_dicom.GetMetaData(DicomTags.IMAGE_POSITION_PATIENT.value).split('\\')[2]
    converted_dicom_name = '{0:.2f}'.format(slice_position + min_position)
    Image.fromarray(image_bytes, 'L').save(converted_dicoms_folder_path + converted_dicom_name + '.png')
