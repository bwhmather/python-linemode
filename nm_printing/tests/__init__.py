import unittest

from nm_printing.tests.test_line_mode_renderer import TestLineModeRenderer


loader = unittest.TestLoader()
suite = unittest.TestSuite((
    loader.loadTestsFromTestCase(TestLineModeRenderer),
))
