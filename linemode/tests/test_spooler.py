import unittest
import threading
from time import sleep

from linemode import PrintSpooler
from linemode.base import Printer


class TestPrintSpooler(unittest.TestCase):
    def test_shutdown(self):
        class DummyPrinter(Printer):
            pass
        spooler = PrintSpooler(DummyPrinter())
        spooler.shutdown()

    def test_shutdown_with_pending(self):
        testcase = self
        condition = threading.Condition()
        executed = False

        class DummyPrinter(Printer):
            def compile(self, commands):
                return None

            def execute(self, program):
                nonlocal testcase
                nonlocal condition
                nonlocal executed

                with condition:
                    condition.wait()

                    # only one job should run
                    testcase.assertFalse(executed)

                    executed = True

        spooler = PrintSpooler(DummyPrinter())
        job_1 = spooler.submit(None)
        job_2 = spooler.submit(None)

        shutdown_thread = threading.Thread(target=spooler.shutdown)
        shutdown_thread.start()

        # first task should still be blocking
        self.assertFalse(executed)

        with condition:
            condition.notify_all()

        shutdown_thread.join()

        # the first print job should have finished before shutting down
        self.assertTrue(executed)
        self.assertTrue(job_1.done())
        self.assertTrue(job_2.cancelled())

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

    def test_execute_fail(self):
        class DummyPrinter(Printer):
            def compile(self, commands):
                return None

            def execute(self, program):
                raise Exception("failed for no good reason")

        spooler = PrintSpooler(DummyPrinter())
        self.assertRaises(Exception, spooler.submit(None).result)

        # TODO better way to check for shutdown
        sleep(0.1)
        self.assertRaises(RuntimeError, spooler.submit, None)
