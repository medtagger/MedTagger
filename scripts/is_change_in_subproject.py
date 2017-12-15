#!/usr/bin/env python
import logging
import os
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Checks if directory contains any change.')
parser.add_argument('directory', type=str, help='Directory in which should be changes.')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO)
commit_range = os.environ.get('TRAVIS_COMMIT_RANGE', '').replace('...', '..')
if not commit_range:
    logging.warn('Could not find a commit range, not doing anything.')
else:
    logging.info('Finding all containers that changed in %s', commit_range)
    diff_lines = subprocess.check_output(['git', 'diff', '--name-only', commit_range]).split()
    changed_folders = {os.path.dirname(line) for line in diff_lines if os.path.dirname(line)}
    logging.info('The following folders contain changes: %s', changed_folders)
    if args.directory in changed_folders:
        exit(0)
    else:
        exit(1)

