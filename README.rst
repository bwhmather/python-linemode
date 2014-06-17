Newman Printing
===============

Example
-------

Basic, without template system:

.. code:: python

    from nm_printing import open_printer

    printer = open_printer('star+lpt:///dev/usb/lp0')

    printer.run_commands([
        ('fontsize-large'),
        ('select-bold'),
        ('write', "Hello world\n"),
        ('cut-through'),
    ])
