#!/usr/bin/env python
import logging
import os
import subprocess
import argparse


def get_root_dir(path):
    return os.path.dirname(path).split('/')[0]

def run():
    exit(0)

def do_not_run():
    exit(1)


logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser(description='Checks if directory contains any change.')
parser.add_argument('subproject_name', type=str, help='Directory in which should be changes.')
args = parser.parse_args()

if os.environ.get('TRAVIS_PULL_REQUEST', False):
    logging.info('This is a Pull Request, so we will run CI only for changed subprojects.')
    diff_lines = subprocess.check_output(['git', 'diff', '--name-only', 'origin/master']).split()
    changed_subprojects = {get_root_dir(line) for line in diff_lines if os.path.dirname(line)}
    logging.info('The following subprojects contain changes: %s', changed_subprojects)
    if args.subproject_name in changed_subprojects:
        run()
    else:
        do_not_run()
else:
    logging.info('Running all tests as it is not a Pull Request.')
    run()

