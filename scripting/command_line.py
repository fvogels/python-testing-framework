import argparse
import sys
import os
import types
from scripting.version import __version__
from scripting.fileutils import find_files_recursively, has_name, execute_code, inside_directory
from scripting.scoring import Score, keep_score
from scripting.counting import keep_counts
from scripting.tested import tested_file
from scripting.reporting import reporting
from scripting.testing import skip


def _version_command(args):
    '''
    Runs when using version command
    '''
    print(__version__)


def _test_command(args):
    '''
    Runs when using test command
    '''
    with keep_score() as current_score, keep_counts() as current_counts, reporting():
        for path_to_tests in find_files_recursively(predicate=has_name(args.tests_file)):
            directory_containing_tests = os.path.dirname(path_to_tests)
            with inside_directory(directory_containing_tests):
                tested_file_present = os.path.isfile(args.tested_file)
                filename_of_tests = os.path.basename(path_to_tests)

                if not tested_file_present:
                    print(f"ERROR: Could not find {args.tested_file} in {os.path.abspath(directory_containing_tests)}")

                    if args.ignore_missing_tested_file:
                        print(f"WARNING: Continuing with testing --- tests will be fully ignored, not even be counted as skipped")
                    else:
                        sys.exit(-1)
                else:
                    with tested_file(args.tested_file):
                        execute_code(os.path.basename(filename_of_tests))

        score = current_score()
        counts = current_counts()

    print(score)
    print(counts)


def create_command_line_arguments_parser():
    '''
    Creates parsers and subparsers
    '''
    # Top level parser
    parser = argparse.ArgumentParser(prog='scripting')
    parser.set_defaults(func=lambda args: parser.print_help())
    subparsers = parser.add_subparsers(help='sub-command help')

    # Version command parser
    test_parser = subparsers.add_parser('version', help='returns version')
    test_parser.set_defaults(func=_version_command)

    # Test command parser
    test_parser = subparsers.add_parser('test', help='runs tests in all subdirectories')
    test_parser.add_argument('--ignore-missing-tested-file', help='If tested file is missing, simply skip tests', action='store_true')
    test_parser.add_argument('--tested-file', help='File where tested code resides (default: student.py)', default='student.py')
    test_parser.add_argument('--tests-file', help='File where tests resides (default: tests.py)', default='tests.py')
    test_parser.set_defaults(func=_test_command)

    return parser


def shell_entry_point():
    '''
    Called from shell using 'scripting' command
    '''
    parser = create_command_line_arguments_parser()
    args = parser.parse_args(sys.argv[1:])

    args.func(args)
