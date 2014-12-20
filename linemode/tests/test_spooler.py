import unittest

from linemode import PrintSpooler
from linemode.base import Printer


class TestPrintSpooler(unittest.TestCase):
    def test_shutdown(self):
        class DummyPrinter(Printer):
            pass
        spooler = PrintSpooler(DummyPrinter())
        spooler.shutdown()

    def test_submit_job(self):
        testcase = self
        dummy_commands = object()
        compiled = False

        dummy_program = object()
        executed = False

        class DummyPrinter(Printer):
            def compile(self, commands):
                nonlocal testcase
                nonlocal dummy_commands
                nonlocal compiled
                nonlocal dummy_program

                testcase.assertIs(commands, dummy_commands)
                testcase.assertFalse(compiled)

                compiled = True

                return dummy_program

            def execute(self, program):
                nonlocal testcase
                nonlocal dummy_program
                nonlocal executed

                testcase.assertIs(program, dummy_program)
                testcase.assertFalse(executed)

                executed = True

        spooler = PrintSpooler(DummyPrinter())
        spooler.submit(dummy_commands)

        spooler.shutdown()

        self.assertTrue(compiled)
        self.assertTrue(executed)
