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

    def test_detect_charset(self):
        printer = StarPrinter(None)

        program = printer.compile([
            ('write', "ぐけげこごさざしじすずせぜそぞた"),
        ])

        self.assertEqual(
            program,
            b'\x1b\x1d\x74' + b'\x02' +
            "ぐけげこごさざしじすずせぜそぞた".encode('euc_jp')
        )
