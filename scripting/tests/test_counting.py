from unittest import TestCase
from scripting.fileutils import find_files_recursively, has_name
from scripting.testing import test, skip_if
from scripting.counting import keep_counts, Counts
from scripting.assertions import fail
from scripting.flow import skip_after_fail, continue_after_fail
from scripting.scoring import keep_score, all_or_nothing


class TestCounting(TestCase):
    def test_single_failing_test(self):
        with keep_counts() as current_count:
            @test()
            def _():
                fail()

            self.assertEqual(current_count(), Counts(0, 1, 0))

    def test_single_passing_test(self):
        with keep_counts() as current_count:
            @test()
            def _():
                pass

            self.assertEqual(current_count(), Counts(1, 0, 0))

    def test_single_skipped_test(self):
        with keep_counts() as current_count, skip_if(True):
            @test()
            def _():
                pass

            self.assertEqual(current_count(), Counts(0, 0, 1))

    def test_skip_after_fail_ppp(self):
        with keep_counts() as current_count, skip_after_fail():
            @test()
            def _():
                pass

            @test()
            def _():
                pass

            @test()
            def _():
                pass

            self.assertEqual(current_count(), Counts(3, 0, 0))

    def test_skip_after_fail_ppf(self):
        with keep_counts() as current_count, skip_after_fail():
            @test()
            def _():
                pass

            @test()
            def _():
                pass

            @test()
            def _():
                fail()

            self.assertEqual(current_count(), Counts(2, 1, 0))

    def test_skip_after_fail_pfp(self):
        with keep_counts() as current_count, skip_after_fail():
            @test()
            def _():
                pass

            @test()
            def _():
                fail()

            @test()
            def _():
                pass

            self.assertEqual(current_count(), Counts(1, 1, 1))

    def test_skip_after_fail_pff(self):
        with keep_counts() as current_count, skip_after_fail():
            @test()
            def _():
                pass

            @test()
            def _():
                fail()

            @test()
            def _():
                fail()

            self.assertEqual(current_count(), Counts(1, 1, 1))

    def test_skip_after_fail_fpp(self):
        with keep_counts() as current_count, skip_after_fail():
            @test()
            def _():
                fail()

            @test()
            def _():
                pass

            @test()
            def _():
                pass

            self.assertEqual(current_count(), Counts(0, 1, 2))

    def test_all_or_nothing_fpp(self):
        with keep_score(), keep_counts() as current_count, all_or_nothing():
            @test()
            def _():
                fail()

            @test()
            def _():
                pass

            @test()
            def _():
                pass

            self.assertEqual(current_count(), Counts(2, 1, 0))

    def test_skip_after_fail_fpp(self):
        with keep_counts() as current_count, skip_after_fail():
            @test()
            def _():
                fail()

            @test()
            def _():
                pass

            @test()
            def _():
                pass

            self.assertEqual(current_count(), Counts(0, 1, 2))

    def test_continue_after_fail_fpp(self):
        with keep_counts() as current_count, continue_after_fail():
            @test()
            def _():
                fail()

            @test()
            def _():
                pass

            @test()
            def _():
                pass

            self.assertEqual(current_count(), Counts(2, 1, 0))

    def test_continue_after_fail_inside_skip_after_fail_fpp(self):
        with keep_counts() as current_count, skip_after_fail(), continue_after_fail():
            @test()
            def _():
                fail()

            @test()
            def _():
                pass

            @test()
            def _():
                pass

            self.assertEqual(current_count(), Counts(2, 1, 0))
