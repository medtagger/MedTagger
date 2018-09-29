"""Script that will fill MedTagger with data.

How to use it?
--------------
At first, download some scans from anywhere on the Internet. You can use example dataset from Data Science Bowl 2017:
https://www.kaggle.com/c/data-science-bowl-2017/data (look for 'sample_images.7z' file).

Then, place these data (unzipped) anywhere on your computer and run this script by:

    (venv) $ python3.7 scripts/import_data.py --source=./dir_with_scans/

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
import logging
import logging.config

from medtagger.repositories import scans as ScansRepository, datasets as DatasetsRepository
from medtagger.workers.storage import parse_dicom_and_update_slice


logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Import data to the MedTagger.')
parser.add_argument('--source', type=str, required=True, help='Source directory')
parser.add_argument('--dataset', type=str, required=True, help='Dataset key for these scans')
args = parser.parse_args()


if __name__ == '__main__':
    logger.info('Checking Dataset...')
    dataset = DatasetsRepository.get_dataset_by_key(args.dataset)

    source = args.source.rstrip('/')
    for scan_directory in glob.iglob(source + '/*'):
        if not os.path.isdir(scan_directory):
            logger.warning('"%s" is not a directory. Skipping...', scan_directory)
            continue

        logger.info('Adding new Scan from "%s".', scan_directory)
        slice_names = glob.glob(scan_directory + '/*.dcm')
        number_of_slices = len(slice_names)
        scan = ScansRepository.add_new_scan(dataset, number_of_slices, None)

        for slice_name in slice_names:
            logger.info('Adding new Slice to Scan "%s" based on "%s".', scan.id, slice_name)
            with open(slice_name, 'rb') as slice_dicom_file:
                _slice = scan.add_slice()
                image = slice_dicom_file.read()
                parse_dicom_and_update_slice.delay(_slice.id, image)
