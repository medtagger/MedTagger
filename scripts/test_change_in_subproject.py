#!/usr/bin/env python
from __future__ import print_function
import logging
import os
import argparse
import subprocess
from subprocess import Popen, PIPE


logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser(description='Checks if directory contains any change.')
parser.add_argument('subproject_name', type=str, help='Directory in which should be changes.')
parser.add_argument('--command', dest='command', type=str, help='Command to be executed if there was a change.')
args = parser.parse_args()


def get_root_dir(path):
    return os.path.dirname(path).split('/')[0]

def run(command):
    logging.info('Let\'s run the CI!')
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    for stdout_line in iter(p.stdout.readline, ""):
        print(stdout_line, end="") 
    p.stdout.close()
    return_code = p.wait()
    exit(returncode)
#    try:
#        subprocess.check_output(command, shell=True)
#    except Exception as e:
#        logging.error(str(e))
#        exit(1)

def do_not_run():
    logging.info('This subproject does not contain changes.')
    exit(0)


if os.environ.get('TRAVIS_PULL_REQUEST', False):
    logging.info('This is a Pull Request, so we will run CI only for changed subprojects.')
    diff_lines = subprocess.check_output(['git', 'diff', '--name-only', 'origin/master']).split()
    changed_subprojects = {get_root_dir(line) for line in diff_lines if os.path.dirname(line)}
    logging.info('The following subprojects contain changes: %s', changed_subprojects)
    if args.subproject_name in changed_subprojects:
        run(args.command)
    else:
        do_not_run()
else:
    logging.info('Running all tests as it is not a Pull Request.')
    run(args.command)

