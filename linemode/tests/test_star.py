import unittest

from linemode.drivers.star import StarPrinter


class TestStarPrinter(unittest.TestCase):
    def test_hello(self):
        printer = StarPrinter(None)

        program = printer.compile([
            ('select-bold'),
            ('write', "Hello World"),
            ('cancel-bold'),
        ])

        self.assertEqual(program, b'\x1b\x45Hello World\x1b\x46')
