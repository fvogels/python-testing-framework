from unittest import TestCase
from scripting.fileutils import find_files_recursively, has_name
from scripting.testing import test, skip_if
from scripting.counting import keep_counts, Counts
from scripting.assertions import fail
from scripting.flow import skip_after_fail, continue_after_fail
from scripting.scoring import keep_score, all_or_nothing


class TestFlow(TestCase):
    def test_fail_interrupts(self):
        a = False

        @test()
        def _():
            nonlocal a
            fail()
            a = True

        self.assertFalse(a)


    def test_ppp(self):
        a = False
        b = False
        c = False

        @test()
        def _():
            nonlocal a
            a = True

        @test()
        def _():
            nonlocal b
            b = True

        @test()
        def _():
            nonlocal c
            c = True

        self.assertTrue(a)
        self.assertTrue(b)
        self.assertTrue(c)

    def test_fpp(self):
        a = False
        b = False
        c = False

        @test()
        def _():
            nonlocal a
            a = True
            fail()

        @test()
        def _():
            nonlocal b
            b = True

        @test()
        def _():
            nonlocal c
            c = True

        self.assertTrue(a)
        self.assertTrue(b)
        self.assertTrue(c)

    def test_skip_after_fail_fpp(self):
        a = False
        b = False
        c = False

        with skip_after_fail():
            @test()
            def _():
                nonlocal a
                a = True
                fail()

            @test()
            def _():
                nonlocal b
                b = True

            @test()
            def _():
                nonlocal c
                c = True

        self.assertTrue(a)
        self.assertFalse(b)
        self.assertFalse(c)

    def test_skip_after_fail_pfp(self):
        a = False
        b = False
        c = False

        with skip_after_fail():
            @test()
            def _():
                nonlocal a
                a = True

            @test()
            def _():
                nonlocal b
                b = True
                fail()

            @test()
            def _():
                nonlocal c
                c = True

        self.assertTrue(a)
        self.assertTrue(b)
        self.assertFalse(c)

    def test_continue_after_fail_pfp(self):
        a = False
        b = False
        c = False

        with continue_after_fail():
            @test()
            def _():
                nonlocal a
                a = True

            @test()
            def _():
                nonlocal b
                b = True
                fail()

            @test()
            def _():
                nonlocal c
                c = True

        self.assertTrue(a)
        self.assertTrue(b)
        self.assertTrue(c)

    def test_continue_after_fail_in_skip_after_fail_pfp(self):
        a = False
        b = False
        c = False

        with skip_after_fail(), continue_after_fail():
            @test()
            def _():
                nonlocal a
                a = True

            @test()
            def _():
                nonlocal b
                b = True
                fail()

            @test()
            def _():
                nonlocal c
                c = True

        self.assertTrue(a)
        self.assertTrue(b)
        self.assertTrue(c)
