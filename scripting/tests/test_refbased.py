from unittest import TestCase
from scripting.fileutils import find_files_recursively, has_name
from scripting.testing import test, skip_if
from scripting.scoring import Score, keep_score, all_or_nothing, cumulative
from scripting.reference import reference_based_testing


class TestScoring(TestCase):
    def test_passing(self):
        def refimpl(x):
            return x

        def testimpl(x):
            return x

        with keep_score() as current_score, reference_based_testing(refimpl, testimpl) as testcase:
            testcase(0)
            testcase(1)
            testcase(2)
            testcase(3)

            self.assertEqual(current_score(), Score(4, 4))

    def test_failing(self):
        def refimpl(x):
            return x

        def testimpl(x):
            return x * 2

        with keep_score() as current_score, reference_based_testing(refimpl, testimpl) as testcase:
            testcase(0)
            testcase(1)
            testcase(2)
            testcase(3)

            self.assertEqual(current_score(), Score(1, 4))

    def test_passing_parameter_modification(self):
        def refimpl(xs):
            return xs.append(1)

        def testimpl(xs):
            return xs.append(1)

        with keep_score() as current_score, reference_based_testing(refimpl, testimpl) as testcase:
            testcase([])
            testcase([1])
            testcase([2])
            testcase([1,2,3])

            self.assertEqual(current_score(), Score(4, 4))

    def test_failing_parameter_modification(self):
        def refimpl(xs):
            return xs.append(1)

        def testimpl(xs):
            return xs.append(2)

        with keep_score() as current_score, reference_based_testing(refimpl, testimpl) as testcase:
            testcase([])
            testcase([1])
            testcase([2])
            testcase([1,2,3])

            self.assertEqual(current_score(), Score(0, 4))
