Python Linemode Printing
========================
.. image:: https://travis-ci.org/bwhmather/python-linemode.png?branch=develop
    :target: http://travis-ci.org/bwhmather/python-linemode
    :alt: Build Status

Python library for communicating with line-mode thermal printers.
Currently works only with printers that support the star line mode protocol but adding support for other similar printers should be possible.

Also provides a module for compiling an xml description of a page to a list of commands.

Developed at `Newman Online Ltd`_ and open sourced with permission.

Examples
--------

Basic, without template system:

.. code:: python

    from linemode import open_printer

    printer = open_printer('star+lpt:///dev/usb/lp0')

    printer.run_commands([
        ('fontsize-large'),
        ('select-bold'),
        ('write', "Hello world\n"),
        ('cut-through'),
    ])

Running templates:

.. code:: python

    from linemode import open_printer
    from linemode.renderers import xml

    printer = open_printer('star+lpt:///dev/usb/lp0')

    printer.run_commands(xml.render("""
    <document>
      <line>
        <bold>Hello world</bold>
      </line>
    </document>
    """))

With jinja:

.. code:: python

    from jinja2 import Template

    from linemode import open_printer
    from linemode.renderers import xml

    printer = open_printer('star+lpt:///dev/usb/lp0')

    # jinja2 template
    template = """
    <document>
      {% for potatoes in [1, 2, 3, 4] %}
      <line>
        {{ potatoes }} potato
      </line>
      {% endfor %}
    </document>
    """
    # line mode printer document
    document = Template(template).render()

    # iterator of generic printer instructions
    commands = xml.render(document)

    # printer specific compiled representation
    program = printer.compile(commands)

    printer.execute(program)

Command Language
----------------

``reset``
  Reset everything to it's initial state.

``select-bold``/``cancel-bold``
  Toggle printing bold text.

``select-highlight``/``cancel-highlight``
  Toggle printing white on black instead of black on white.

``fontsize-small``/``fontsize-medium``/``fontsize-large``
  Set the line height for the current line and all following lines.
  If not sent at the beginning of a new line then behaviour is undefined.
  Characters should remain the same width.

  Default: ``fontsize-small``

``write <string>``
  Print the contents of a unicode string.
  If any characters are unsupported, they will be replaced with '?'.

``barcode <style> <data>``
  TODO

``newline``
  Flush the line buffer and start a new line.

``cut-through``
  Create a cut at the next mark

``cut-partial``
  Create a perforated cut at the next mark

``cut-through-immediate``
  Create a cut at the current cursor position

``cut-partial-immediate``
  Create a perforated cut at the current cursor position

Bugs
----

Please post any problems or feature requests using the `issue tracker`_.
Pull requests welcome.
New drivers would be greatly appreciated.

.. _Newman Online Ltd: http://newmanonline.org.uk
.. _issue tracker: https://github.com/bwhmather/verktyg/issues
