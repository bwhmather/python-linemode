import unittest

from linemode.renderers.command_list import render


class TestCommandListRenderer(unittest.TestCase):
    def test_simple_command(self):
        commands = list(render(
            "reset"
        ))
        self.assertEqual(commands, ["reset"])

    def test_comments(self):
        commands = list(render(
            "# this is a comment\n"
            "reset\n"
            "# comment"
        ))
        self.assertEqual(commands, ["reset"])

    def test_blank_lines(self):
        commands = list(render(
            "\n"
            "reset\n"
            "\n"
        ))
        self.assertEqual(commands, ["reset"])

    def test_single_arg(self):
        commands = list(render("write: 'hello world'"))
        self.assertEqual(commands, [("write", 'hello world')])

    def test_multiple_args(self):
        commands = list(render("barcode: 'EAN-8', '12345678'"))
        self.assertEqual(commands, [("barcode", "EAN-8", "12345678")])
