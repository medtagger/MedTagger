"""Script that will fill your HBase database with data.

How to use it?
--------------
At first, download some scans from anywhere on the Internet. You can use example dataset from Data Science Bowl 2017:
https://www.kaggle.com/c/data-science-bowl-2017/data (look for 'sample_images.7z' file).

Then, place these data (unzipped) anywhere on your computer and run this script by:

    (venv) $ python3.6 scripts/import_data.py --source=./dir_with_scans/

Please keep all scans with given structure:

    |
    `-- dir_with_scans
        |-- 0a0c32c9e08cc2ea76a71649de56be6d
        |   |-- 0a67f9edb4915467ac16a565955898d3.dcm
        |   |-- 0eb4e3cae3de93e50431cf12bdc6c93d.dcm
        |   `-- ...
        |-- 0a38e7597ca26f9374f8ea2770ba870d
        |   |-- 0bad9c3a3890617f78a905b78bc60f99.dcm
        |   |-- 1cffdd431884c2792ae0cbecec1c9e14.dcm
        |   `-- ...
        `-- ...

"""
import os
import argparse
import glob

from data_labeling.database import db_session
from data_labeling.database.models import Scan, ScanCategory
from data_labeling.workers.conversion import convert_dicom_to_png
from data_labeling.workers.storage import store_dicom


parser = argparse.ArgumentParser(description='Import data to the HBase Database.')
parser.add_argument('--source', type=str, required=True, help='Source directory')
parser.add_argument('--category', type=str, required=True, help='Category key for these scans')
args = parser.parse_args()


if __name__ == '__main__':
    with db_session() as session:
        category = session.query(ScanCategory).filter(ScanCategory.key == args.category).one()

    source = args.source.rstrip('/')
    for scan_directory in glob.iglob(source + '/*'):
        if not os.path.isdir(scan_directory):
            continue

        print('Adding new scan from {}.'.format(scan_directory))
        with db_session() as session:
            scan = Scan(category)
            session.add(scan)

        for slice_name in glob.iglob(scan_directory + '/*.dcm'):
            print('Adding new slice to scan {} based on {}.'.format(scan.id, slice_name))
            with open(slice_name, 'rb') as slice_dicom_file:
                image = slice_dicom_file.read()
                _slice = scan.add_slice()
                store_dicom.delay(_slice.id, image)
                convert_dicom_to_png.delay(_slice.id, image)
