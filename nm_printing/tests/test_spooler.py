import unittest

from nm_printing import PrintSpooler
from nm_printing.base import Printer


class TestPrintSpooler(unittest.TestCase):
    def test_shutdown(self):
        class DummyPrinter(Printer):
            pass
        spooler = PrintSpooler(DummyPrinter())
        spooler.shutdown()
