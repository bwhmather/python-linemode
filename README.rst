Python Linemode Printing
========================
.. image:: https://travis-ci.org/bwhmather/python-linemode.svg?branch=develop :target: https://travis-ci.org/bwhmather/python-linemode

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
    from linemode.renderers import line_mode

    printer = open_printer('star+lpt:///dev/usb/lp0')

    printer.run_commands(line_mode.render("""
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
    from linemode.renderers import line_mode

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
    commands = line_mode.render(document)

    # printer specific compiled representation
    program = printer.compile(commands)

    printer.execute(program)

Bugs
----

Please post any problems or feature requests using the `issue tracker`_.
Pull requests welcome.
New drivers would be greatly appreciated.

.. _Newman Online Ltd: http://newmanonline.org.uk
.. _issue tracker: https://github.com/bwhmather/verktyg/issues
