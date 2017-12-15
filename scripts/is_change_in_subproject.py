#!/usr/bin/env python
import logging
import os
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Checks if directory contains any change.')
parser.add_argument('directory', type=str, help='Directory in which should be changes.')
args = parser.parse_args()
print(args.directory)

logging.basicConfig(level=logging.INFO)
if os.environ.get('TRAVIS_PULL_REQUEST', False):
    commit_range = 'master..' + os.environ.get('TRAVIS_COMMIT', '')
    logging.info('Finding all containers that changed in %s', commit_range)
    diff_lines = subprocess.check_output(['git', 'diff', '--name-only', 'origin/master']).split()
    print(diff_lines)
    changed_folders = {os.path.dirname(line) for line in diff_lines if os.path.dirname(line)}
    print(changed_folders)
    logging.info('The following folders contain changes: %s', changed_folders)
    if args.directory in changed_folders:
        exit(0)
    else:
        exit(1)
else:
    logging.info('Running all tests as it is not a Pull Request.')
    exit(0)

