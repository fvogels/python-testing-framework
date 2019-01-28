from unittest import TestCase
from scripting.fileutils import find_files_recursively, has_name
from scripting.testing import test, skip_if
from scripting.scoring import Score, keep_score, all_or_nothing, cumulative
from scripting.assertions import fail


class TestScoring(TestCase):
    def test_single_failing_test(self):
        with keep_score() as current_score:
            @test()
            def _():
                fail()

            self.assertEqual(current_score(), Score(0, 1))

    def test_single_passing_test(self):
        with keep_score() as current_score:
            @test()
            def _():
                pass

            self.assertEqual(current_score(), Score(1, 1))

    def test_single_skipped_test(self):
        with keep_score() as current_score, skip_if(True):
            @test()
            def _():
                pass

            self.assertEqual(current_score(), Score(0, 1))

    def test_pass_pass(self):
        with keep_score() as current_score:
            @test()
            def _():
                pass

            @test()
            def _():
                pass

            self.assertEqual(current_score(), Score(2, 2))

    def test_pass_fail(self):
        with keep_score() as current_score:
            @test()
            def _():
                pass

            @test()
            def _():
                fail()

            self.assertEqual(current_score(), Score(1, 2))

    def test_fail_pass(self):
        with keep_score() as current_score:
            @test()
            def _():
                fail()

            @test()
            def _():
                pass

            self.assertEqual(current_score(), Score(1, 2))

    def test_fail_fail(self):
        with keep_score() as current_score:
            @test()
            def _():
                fail()

            @test()
            def _():
                fail()

            self.assertEqual(current_score(), Score(0, 2))

    def test_all_or_nothing_ff(self):
        with keep_score() as current_score:
            with all_or_nothing():
                @test()
                def _():
                    fail()

                @test()
                def _():
                    fail()

            self.assertEqual(current_score(), Score(0, 2))

    def test_all_or_nothing_pf(self):
        with keep_score() as current_score:
            with all_or_nothing():
                @test()
                def _():
                    pass

                @test()
                def _():
                    fail()

            self.assertEqual(current_score(), Score(0, 2))

    def test_all_or_nothing_fp(self):
        with keep_score() as current_score:
            with all_or_nothing():
                @test()
                def _():
                    fail()

                @test()
                def _():
                    pass

            self.assertEqual(current_score(), Score(0, 2))

    def test_all_or_nothing_pp(self):
        with keep_score() as current_score:
            with all_or_nothing():
                @test()
                def _():
                    pass

                @test()
                def _():
                    pass

            self.assertEqual(current_score(), Score(2, 2))

    def test_cumulative_in_all_or_nothing(self):
        with keep_score() as current_score:
            with all_or_nothing():
                with cumulative():
                    @test()
                    def _():
                        pass

                    @test()
                    def _():
                        fail()

                with cumulative():
                    @test()
                    def _():
                        pass

                    @test()
                    def _():
                        fail()

            self.assertEqual(current_score(), Score(0, 4))