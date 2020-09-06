import pytest
from dockernel.cli import set_subcommand_func, run_subcommand
from argparse import ArgumentParser


class TestFuncSettingOnParsers:
    @pytest.fixture
    def parser(self):
        return ArgumentParser()

    def test_run_subcommand_calls_set_func(self, parser):
        called = False

        def call_me(*_):
            nonlocal called
            called = True

        set_subcommand_func(parser, call_me)
        run_subcommand(parser.parse_args([]))

        assert called

    def test_run_subcommand_returns_from_func(self, parser):
        return_value = 123

        def func(*_):
            return return_value

        set_subcommand_func(parser, func)
        returned = run_subcommand(parser.parse_args([]))

        assert returned == return_value

    def test_run_subcommand_passes_parsed_args_to_func(self, parser):
        def func(passed_args):
            assert passed_args is parsed_args

        set_subcommand_func(parser, func)
        parsed_args = parser.parse_args()
        run_subcommand(parsed_args)
