from unittest import TestCase
from scripting.fileutils import find_files_recursively, has_name
from scripting.testing import initialize_testing_environment, test, skip_if
from scripting.scoring import Score, keep_score, current_score
from scripting.assertions import fail


class TestScoring(TestCase):
    def test_single_failing_test(self):
        with initialize_testing_environment(), keep_score():
            @test()
            def _():
                fail()

            self.assertEqual(current_score(), Score(0, 1))

    def test_single_passing_test(self):
        with initialize_testing_environment(), keep_score():
            @test()
            def _():
                pass

            self.assertEqual(current_score(), Score(1, 1))

    def test_single_skipped_test(self):
        with initialize_testing_environment(), keep_score(), skip_if(True):
            @test()
            def _():
                pass

            self.assertEqual(current_score(), Score(0, 1))

    def test_pass_pass(self):
        with initialize_testing_environment(), keep_score():
            @test()
            def _():
                pass

            @test()
            def _():
                pass

            self.assertEqual(current_score(), Score(2, 2))

    def test_pass_fail(self):
        with initialize_testing_environment(), keep_score():
            @test()
            def _():
                pass

            @test()
            def _():
                fail()

            self.assertEqual(current_score(), Score(1, 2))

    def test_fail_pass(self):
        with initialize_testing_environment(), keep_score():
            @test()
            def _():
                fail()

            @test()
            def _():
                pass

            self.assertEqual(current_score(), Score(1, 2))

    def test_fail_fail(self):
        with initialize_testing_environment(), keep_score():
            @test()
            def _():
                fail()

            @test()
            def _():
                fail()

            self.assertEqual(current_score(), Score(0, 2))