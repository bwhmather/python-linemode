Python Linemode Printing
========================
.. image:: https://travis-ci.org/bwhmather/python-linemode.svg?branch=develop :target: https://travis-ci.org/bwhmather/python-linemode




Example
-------

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

