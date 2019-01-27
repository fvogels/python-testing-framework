import argparse
import sys
import scripting
import types
from scripting.version import __version__
from scripting.fileutils import find_files_recursively, has_name
from scripting.testing import initialize_testing_environment
from scripting.scoring import Score, keep_score



def __version_command(args):
    '''
    Runs when using version command
    '''
    print(__version__)


def __test_command(args):
    '''
    Runs when using test command
    '''
    score = Score(0, 0)

    def score_receiver(s):
        nonlocal score
        score = s

    with initialize_testing_environment(), keep_score(score_receiver):
        for filename in find_files_recursively(predicate=has_name('tests.py')):
            test_module = types.ModuleType('tests')

            with open(filename, 'r') as file:
                code = file.read()
                exec(code, test_module.__dict__)

    print(score)


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
    test_parser.set_defaults(func=__version_command)

    # Test command parser
    test_parser = subparsers.add_parser('test', help='runs tests in all subdirectories')
    test_parser.set_defaults(func=__test_command)

    return parser


def shell_entry_point():
    '''
    Called from shell using 'scripting' command
    '''
    parser = create_command_line_arguments_parser()
    args = parser.parse_args(sys.argv[1:])

    args.func(args)
