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

### `<bold>`

"""
import re


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


class _LineModeRenderer(object):
    def __init__(self, source, *, max_width=None, prelude=True):
        self._source = source
        self._max_width = max_width
        self._prelude = prelude

        self._bold_stack = 0
        self._highlight_stack = 0

        try:
            import lxml
            assert lxml
        except ImportError as e:
            raise ImportError(
                "lxml not installed.  "
                "Please install nm-printing with the XMLRenderer flag."
            ) from e

        # TODO this seems funky
        self._generator = self._render()

    def _body_width(self, elem, *, max_width=None):
            width = len(elem.text or '')
            if max_width is not None:
                if width > max_width:
                    return max_width

                for child in elem.getchildren():
                    width += self._element_width(
                        child, max_width=max_width - width
                    )

                    width += len(child.tail or '')

                    if width > max_width:
                        return max_width
            else:
                for child in elem.getchildren():
                    width += self._element_width(child)
                    width += len(child.tail or '')

            return width

    def _span_width(self, elem, *, max_width=None):
        if 'width' in elem.attrib:
            width = int(elem.attrib['width'])
            if max_width is not None:
                width = min(width, max_width)
            return width

        # TODO right to left filling
        alignment = elem.attrib.get('align', 'left')
        if alignment in {'right', 'centerLeft', 'centerRight', 'center'}:
            if max_width is not None:
                return max_width

        return self._body_width(elem, max_width=max_width)

    def _element_width(self, elem, *, max_width=None):
        if elem.tag in {'span', 'bold', 'highlight'}:
            width = self._span_width(elem, max_width=max_width)
        else:
            raise Exception('unknown element', elem)

        if max_width is not None:
            assert width <= max_width
        return width

    def _render_bold(self, elem, *, max_width=None):
        self._bold_stack += 1
        if self._bold_stack == 1:
            yield ('select-bold')

        yield from self._render_body(elem, max_width=max_width)

        self._bold_stack -= 1
        if self._bold_stack == 0:
            yield ('cancel-bold')

    def _render_highlight(self, elem, *, max_width=None):
        self._highlight_stack += 1
        if self._highlight_stack == 1:
            yield ('select-highlight')

        yield from self._render_body(elem, max_width=max_width)

        self._highlight_stack -= 1
        if self._highlight_stack == 0:
            yield ('cancel-highlight')

    def _render_span(self, elem, *, max_width=None):
        width = self._span_width(elem, max_width=max_width)
        body_width = self._body_width(elem, max_width=width)

        if body_width >= width:
            # no point in trying to justify text that overflows. Just align
            # left and truncate rather than trying to truncate at the start
            alignment = 'left'
        else:
            alignment = elem.attrib.get('align', 'left')

        if alignment == 'left':
            left_padding = 0
        elif alignment == 'right':
            left_padding = width - body_width
        elif alignment == 'centerLeft' or alignment == 'center':
            left_padding = (width - body_width) // 2
        elif alignment == 'centerRight':
            left_padding = int(round((width - body_width) / 2))

        if left_padding > 0:
            yield ('write', ' ' * left_padding)

        yield from self._render_body(elem, max_width=width)

        right_padding = width - body_width - left_padding
        if right_padding > 0:
            yield ('write', ' ' * right_padding)

    def _render_body(self, elem, *, max_width=None):
        if max_width is None:
            max_width = self._body_width(elem)

        children = elem.getchildren()

        if elem.text is not None and len(elem.text):
            yield ('write', elem.text[:max_width])

            max_width -= len(elem.text)
            if max_width <= 0:
                return

        for child in children:
            yield from self._render_element(child, max_width=max_width)
            max_width -= self._element_width(child, max_width=max_width)

            assert max_width >= 0

            if max_width == 0:
                return

            if child.tail is not None and len(child.tail):
                yield ('write', child.tail[:max_width])

                max_width -= len(child.tail)
                if max_width <= 0:
                    return

    def _render_element(self, elem, *, max_width=None):
        yield from {
            'span': self._render_span,
            'bold': self._render_bold,
            'highlight': self._render_highlight,
        }[elem.tag](elem, max_width=max_width)

    def _render(self):
        # imported here as lxml is an `extras_require` dependency
        from lxml import etree

        xml = etree.fromstring(self._source)

        _strip_outer_whitespace(xml)
        _compress_whitespace(xml)

        if self._prelude:
            yield ('reset')
            yield ('set-charset', xml.attrib.get('charset', 'ascii'))

        for line in xml.getchildren():
            height = int(line.attrib.get('height', '1'))
            if height != 1:
                yield {
                    2: ('fontsize-medium'),
                    3: ('fontsize-large'),
                }[height]

            yield from self._render_body(line, max_width=self._max_width)
            yield ('write', "\n")

            if height != 1:
                yield ('fontsize-small')

        # TODO better name for flag
        if self._prelude:
            yield ('cut-through')

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._generator)


def render(source, *, max_width=None, prelude=True):
    return _LineModeRenderer(source, max_width=max_width, prelude=prelude)
