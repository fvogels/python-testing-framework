from unittest import TestCase
from scripting.fileutils import load_code_from_file_into_module
from scripting.scoring import Score, keep_score, all_or_nothing, cumulative
from scripting.fileutils import load_code_from_string_into_module
from scripting.quick import reference_based_test
from scripting.reference import reference_module
from scripting.tested import tested_module
from textwrap import dedent


class TestScoring(TestCase):
    def test_passing(self):
        expected = '''
        def foo(x):
            return x * 2
        '''

        actual = '''
        def foo(x):
            return x * 2
        '''

        expected = load_code_from_string_into_module(dedent(expected), 'expected')
        actual = load_code_from_string_into_module(dedent(actual), 'actual')

        with reference_module(expected), tested_module(actual), keep_score() as current_score, reference_based_test('foo') as testcase:
            testcase(0)
            testcase(1)
            testcase(2)
            testcase(3)

            self.assertEqual(current_score(), Score(4, 4))

    def test_failing(self):
        expected = '''
        def foo(x):
            return x * 2
        '''

        actual = '''
        def foo(x):
            return x
        '''

        expected = load_code_from_string_into_module(dedent(expected), 'expected')
        actual = load_code_from_string_into_module(dedent(actual), 'actual')

        with reference_module(expected), tested_module(actual), keep_score() as current_score, reference_based_test('foo') as testcase:
            testcase(0)
            testcase(1)
            testcase(2)
            testcase(3)

            self.assertEqual(current_score(), Score(1, 4))
