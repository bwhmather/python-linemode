import unittest

from linemode import open_printer, register_driver


class TestLoader(unittest.TestCase):
    def test_open_test_driver(self):
        handle = object()

        def test_driver(uri):
            return handle

        register_driver('opentestdriver', test_driver)

        self.assertIs(open_printer('opentestdriver://'), handle)

    def test_no_scheme(self):
        self.assertRaises(ValueError, open_printer, 'example.com')

    def test_not_supported(self):
        self.assertRaises(Exception, open_printer, 'ftp://')
