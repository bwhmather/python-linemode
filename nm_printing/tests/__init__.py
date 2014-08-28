import unittest

from nm_printing.tests.test_line_mode_renderer import TestLineModeRenderer
from nm_printing.tests.test_star import TestStarPrinter


loader = unittest.TestLoader()
suite = unittest.TestSuite((
    loader.loadTestsFromTestCase(TestLineModeRenderer),
    loader.loadTestsFromTestCase(TestStarPrinter),
))
