import unittest

from linemode.tests.test_xml_renderer import TestXMLRenderer
from linemode.tests.test_command_list_renderer import TestCommandListRenderer
from linemode.tests.test_star import TestStarPrinter
from linemode.tests.test_spooler import TestPrintSpooler


loader = unittest.TestLoader()
suite = unittest.TestSuite((
    loader.loadTestsFromTestCase(TestXMLRenderer),
    loader.loadTestsFromTestCase(TestCommandListRenderer),
    loader.loadTestsFromTestCase(TestStarPrinter),
    loader.loadTestsFromTestCase(TestPrintSpooler),
))
