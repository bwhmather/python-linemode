import unittest

from linemode.tests import (
    test_loader,
    test_xml_renderer, test_command_list_renderer,
    test_star, test_command_list_printer,
    test_spooler,
)


loader = unittest.TestLoader()
suite = unittest.TestSuite((
    loader.loadTestsFromModule(test_loader),
    loader.loadTestsFromModule(test_xml_renderer),
    loader.loadTestsFromModule(test_command_list_printer),
    loader.loadTestsFromModule(test_star),
    loader.loadTestsFromModule(test_spooler),
))
