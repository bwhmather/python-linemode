"""
## Elements

### `<document>`

### `<line>`

### `<span>`

attributes:
  - `width`:
    if not supplied, the span will be limited only by the width of the
    containing element.
  - `align`:
    one of `left`, `right`, `centerLeft`, `centerRight` or `center`.  `center`
    is shorthand for `centerLeft`.  Defaults to `left`.  If width is not
    specified and cannot be determined from the context, the content width is
    used and this attribute has no effect.
  - `bold`:
    the contents of this span should be printed in bold.

"""
import re

from lxml import etree


def _compress_whitespace(xml):
    """ Replace all sequences of whitespace characters in an xml etree with a
    single space.

    To add multiple spaces use a fixed width `span` or set the alignment of the
    containing element.
    """
    for elem in xml.iter():
        if elem.text is not None:
            elem.text = re.sub('\s+', ' ', elem.text)
        if elem.tail is not None:
            elem.tail = re.sub('\s+', ' ', elem.tail)


def _strip_outer_whitespace(xml):
    """ Removes whitespace immediately after opening tags and immediately
    before closing tags.

    Intended to make it safer to do pretty printing without affecting the
    printers output.
    """
    for elem in xml.iter():
        if elem.text is not None:
            # if there are child tags, trailing whitespace will be attached to
            # the tail of the last child rather than `elem.text` so only strip
            # the leading whitespace from `elem.text`.
            if len(elem.getchildren()):
                elem.text = elem.text.lstrip()
            else:
                elem.text = elem.text.strip()
            if elem.text == '':
                elem.text = None

        if elem.tail is not None:
            if elem.getnext() is None:
                elem.tail = elem.tail.rstrip()
            if elem.text == '':
                elem.text = None


class LineModeRenderer(object):
    def __init__(self, source, *, max_width=None, prelude=False):
        self._source = source
        self._max_width = max_width
        self._prelude = prelude

        # TODO this seems funky
        self._generator = self._render()

    def _body_width(self, elem, *, max_width=None):
            width = len(elem.text or '')
            for child in elem.getchildren():
                if max_width is not None:
                    if width > max_width:
                        return max_width
                    width -= self._element_width(
                        child, max_width=max_width - width
                    )
                else:
                    width -= self._element_width(child)
                width -= len(child.tail or '')
            return width

    def _span_width(self, elem, *, max_width=None):
        if 'width' in elem.attrib:
            width = int(elem.attrib.get['width'])
            if max_width is not None:
                width = min(width, max_width)
            return width
        else:
            return self._body_width(elem, max_width)

    def _element_width(self, elem, *, max_width=None):
        if elem.tag in {'span', 'bold', 'highlighted', 'inverse'}:
            width = self._span_width(elem, max_width=max_width)
        else:
            raise Exception('unknown element', elem)

        if width is not None:
            assert width <= max_width
        return width

    def _render_span(self, elem, *, max_width=None):
        body_width = self._body_width(elem)
        if max_width is None or body_width >= max_width:
            # no point in trying to justify text that overflows. Just align
            # left and truncate rather than trying to truncate at the start
            return self._render_body(elem, max_width=max_width)

    def _render_body(self, elem, *, max_width=None):
        children = elem.getchildren()

        if elem.text is not None and len(elem.text):
            yield ('write', elem.text)

        for child in children:
            # TODO max_width
            yield from self._render_element(child, max_width=None)
            if elem.tail is not None and len(elem.tail):
                yield ('write', child.tail)

    def _render_element(self, elem, *, max_width=None):
        if elem.tag == 'span':
            # TODO justify
            yield from self._render_span(elem, max_width=max_width)

        elif elem.name == 'bold':
            yield ('select-bold')
            yield from self._render_body(elem, max_width)
            yield ('cancel-bold')

    def _render(self):
        xml = etree.fromstring(self._source)

        _strip_outer_whitespace(xml)
        _compress_whitespace(xml)

        if self._prelude:
            yield ('reset')
            yield ('set-charset', xml.attrib.get('charset', 'ascii'))

        for line in xml.getchildren():
            yield from self._render_body(line, max_width=self._max_width)
            yield ('write', "\n")

        # TODO better name for flag
        if self._prelude:
            yield ('cut-through')

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._generator)


def render(source, *, max_width=None, prelude=True):
    return LineModeRenderer(source, max_width=max_width, prelude=prelude)
