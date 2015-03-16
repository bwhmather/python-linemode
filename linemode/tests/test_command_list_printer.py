import io
import tempfile
import unittest

from linemode.drivers.command_list import (
    compile, CommandListPrinter, open_file
)


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

    def test_printer(self):
        with io.BytesIO() as output, CommandListPrinter(output) as printer:
            printer.run_commands([
                ('write', "hello world"),
            ])

            self.assertEqual(output.getvalue(), b"write: 'hello world'")

    def test_open_file(self):
        with tempfile.NamedTemporaryFile('rb') as output:
            filename = 'commands+file://%s' % output.name

            with open_file(filename) as printer:
                printer.run_commands([
                    ('write', "hello world"),
                ])

            self.assertEqual(output.read(), b"write: 'hello world'")
