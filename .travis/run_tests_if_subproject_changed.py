import argparse
import os
import logging
import subprocess


logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser(description='Checks if directory contains any change.')
parser.add_argument('subproject_name', type=str, help='Directory in which should be changes.')
parser.add_argument('--command', dest='command', type=str, help='Command to be executed if there was a change.')
args = parser.parse_args()

BRANCHES_WITH_FULL_TESTS = ['master']


def get_root_dir(path):
    return os.path.dirname(path).decode().split('/')[0]


def run(command):
    print('=============================')
    print('        TESTS OUTPUT         ')
    print('=============================')
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    while True:
        output = process.stdout.readline().decode()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    print('=============================')
    process.stdout.close()
    return_code = process.poll()
    exit(return_code)


def do_not_run():
    logging.info('This subproject does not contain changes.')
    exit(0)


branch_name = os.environ.get('TRAVIS_BRANCH')
logging.info('Running CI tests on branch "%s".', branch_name)
logging.info('Full testing on all subprojects run on these branches: %s.', BRANCHES_WITH_FULL_TESTS)
if os.environ.get('TRAVIS_BRANCH') not in BRANCHES_WITH_FULL_TESTS:
    logging.info('This is not a fully testing branch, so we will run tests only for changed subprojects.')
    diff_lines = subprocess.check_output(['git', 'diff', '--name-only', 'origin/master']).split()
    changed_subprojects = {get_root_dir(line) for line in diff_lines if os.path.dirname(line)}
    logging.info('The following subprojects contain changes: %s', changed_subprojects)
    if args.subproject_name in changed_subprojects:
        run(args.command)
    else:
        do_not_run()
else:
    logging.info('Running all tests on this branch.')
    run(args.command)

