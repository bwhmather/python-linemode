import unittest

from linemode import PrintSpooler
from linemode.base import Printer


class TestPrintSpooler(unittest.TestCase):
    def test_shutdown(self):
        class DummyPrinter(Printer):
            pass
        spooler = PrintSpooler(DummyPrinter())
        spooler.shutdown()
