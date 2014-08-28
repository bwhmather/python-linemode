import unittest

from nm_printing.tests.test_line_mode_renderer import TestLineModeRenderer
from nm_printing.tests.test_star import TestStarPrinter
from nm_printing.tests.test_spooler import TestPrintSpooler


loader = unittest.TestLoader()
suite = unittest.TestSuite((
    loader.loadTestsFromTestCase(TestLineModeRenderer),
    loader.loadTestsFromTestCase(TestStarPrinter),
    loader.loadTestsFromTestCase(TestPrintSpooler),
))
