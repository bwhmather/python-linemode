import unittest

from linemode.drivers.command_list import compile


class TestCommandListPrinter(unittest.TestCase):
    def test_simple_command(self):
        program = compile([
            "reset"
        ])
        self.assertEqual(program, b'reset')

    def test_single_arg(self):
        program = compile([
            ('write', "hello world"),
        ])
        self.assertEqual(program, b"write: 'hello world'")

    def test_multiple_args(self):
        program = compile([
            ('barcode', "EAN-8", "12345678")
        ])
        self.assertEqual(program, b"barcode: 'EAN-8', '12345678'")

    def test_multiple_commands(self):
        program = compile([
            'reset',
            'select-bold',
            ('write', "HELLO WORLD"),
        ])
        self.assertEqual(program, b"reset\nselect-bold\nwrite: 'HELLO WORLD'")
