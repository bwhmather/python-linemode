import unittest

from linemode.tests.test_line_mode_renderer import TestLineModeRenderer
from linemode.tests.test_star import TestStarPrinter
from linemode.tests.test_spooler import TestPrintSpooler


loader = unittest.TestLoader()
suite = unittest.TestSuite((
    loader.loadTestsFromTestCase(TestLineModeRenderer),
    loader.loadTestsFromTestCase(TestStarPrinter),
    loader.loadTestsFromTestCase(TestPrintSpooler),
))
