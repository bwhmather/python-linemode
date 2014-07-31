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
