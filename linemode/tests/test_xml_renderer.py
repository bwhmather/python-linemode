import unittest
from lxml import etree

from linemode.renderers.xml import (
    _compress_whitespace, _strip_outer_whitespace, render,
)


class TestXMLRenderer(unittest.TestCase):
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
                ('newline'),
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
                ('newline'),
            ]
        )

    def test_align(self):
        def test(alignment, expected):
            commands = list(render("""
            <document>
              <line>
                <span align="%s" width="5">aa</span>
              </line>
            </document>""" % alignment, prelude=False))
            self.assertEqual(commands, expected)

        test('left', [
            ('write', 'aa'), ('write', '   '), ('newline'),
        ])
        test('right', [
            ('write', '   '), ('write', 'aa'), ('newline'),
        ])
        test('centerLeft', [
            ('write', ' '), ('write', 'aa'), ('write', '  '), ('newline'),
        ])
        test('center', [
            ('write', ' '), ('write', 'aa'), ('write', '  '), ('newline'),
        ])
        test('centerRight', [
            ('write', '  '), ('write', 'aa'), ('write', ' '), ('newline'),
        ])

    def test_stretch(self):
        commands = list(render("""
        <document>
          <line>
            <span width="12">
              <span align="left">left</span><span align="right">right</span>
            </span>
          </line>
        </document>
        """, prelude=False))

        self.assertEqual(
            commands,
            [
                ('write', "left"),
                ('write', "   "),
                ('write', "right"),
                ('newline'),
            ]
        )

    def test_overlapping_stretch(self):
        commands = list(render("""
        <document>
          <line>
            <span width="8">
              <span align="left">left</span>
              <span align="right">right</span>
            </span>
          </line>
        </document>
        """, prelude=False))

        self.assertEqual(
            commands,
            [
                ('write', "left"),
                ('write', " "),
                ('write', "rig"),
                ('newline'),
            ]
        )

    def test_bold(self):
        commands = list(render("""
        <document>
          <line>
            <bold>BOLD</bold>
          </line>
        </document>
        """, prelude=False))
        self.assertEqual(
            commands,
            [
                ('select-bold'),
                ('write', "BOLD"),
                ('cancel-bold'),
                ('newline'),
            ]
        )

    def test_nested_bold(self):
        commands = list(render("""
        <document>
          <line>
            <bold>
              <bold>BOLD</bold>STILL BOLD
            </bold>
          </line>
        </document>
        """, prelude=False))
        self.assertEqual(
            commands,
            [
                ('select-bold'),
                ('write', "BOLD"),
                ('write', "STILL BOLD"),
                ('cancel-bold'),
                ('newline'),
            ]
        )

    def test_highlight(self):
        commands = list(render("""
        <document>
          <line>
            <highlight>BOLD</highlight>
          </line>
        </document>
        """, prelude=False))
        self.assertEqual(
            commands,
            [
                ('select-highlight'),
                ('write', "BOLD"),
                ('cancel-highlight'),
                ('newline'),
            ]
        )

    def test_nested_highlight(self):
        commands = list(render("""
        <document>
          <line>
            <highlight>
              <highlight>BOLD</highlight>STILL BOLD
            </highlight>
          </line>
        </document>
        """, prelude=False))
        self.assertEqual(
            commands,
            [
                ('select-highlight'),
                ('write', "BOLD"),
                ('write', "STILL BOLD"),
                ('cancel-highlight'),
                ('newline'),
            ]
        )
