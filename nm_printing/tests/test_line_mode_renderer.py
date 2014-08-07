import unittest
from lxml import etree

from nm_printing.renderers.line_mode import (
    _compress_whitespace, _strip_outer_whitespace, render,
)


class TestLineModeRenderer(unittest.TestCase):
    def test_compress_whitespace(self):
        xml = etree.fromstring("""
        <line>
          <span>
            Word \t<bold>bold</bold>
          </span>
        </line>
        """)
        _compress_whitespace(xml)
        self.assertEqual(
            etree.tostring(xml).decode('utf-8'),
            "<line> <span> Word <bold>bold</bold> </span> </line>"
        )

    def test_strip_outer_whitespace(self):
        def test(src, expected):
            xml = etree.fromstring(src)
            _strip_outer_whitespace(xml)
            self.assertEqual(
                etree.tostring(xml).decode('utf-8'),
                expected
            )

        test("<a> </a>", "<a/>")

        test("<a> text</a>", "<a>text</a>")

        test("<a>text </a>", "<a>text</a>")

        test("<a> <b></b> </a>", "<a><b/></a>")

        test("<a><b> </b></a>", "<a><b/></a>")

        test("<a> text <b></b></a>", "<a>text <b/></a>")

        test("<a><b></b> text <c></c></a>", "<a><b/> text <c/></a>")

        test("<a><b></b> text </a>", "<a><b/> text</a>")

    def test_render_hello(self):
        commands = list(render("""
        <document>
          <line>
            Hello world
          </line>
        </document>
        """, prelude=False))

        self.assertEqual(
            commands,
            [
                ('write', "Hello world"),
                ('write', "\n"),
            ]
        )

    def test_render_span(self):
        commands = list(render("""
        <document>
          <line>
            <span>Hello world</span>
          </line>
        </document>
        """, prelude=False))

        self.assertEqual(
            commands,
            [
                ('write', "Hello world"),
                ('write', "\n"),
            ]
        )

    def test_default_charset(self):
        commands = set(render("""<document></document>"""))
        self.assertIn(('set-charset', 'ascii'), commands)

    def test_charset(self):
        commands = set(render(
            """<document charset="euc_jp"></document>"""
        ))
        self.assertIn(('set-charset', 'euc_jp'), commands)
