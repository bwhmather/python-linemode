from urllib.parse import urlparse

from linemode.base import Printer


def compile(commands):
    # TODO
    raise NotImplementedError()


class CommandListPrinter(Printer):
    def __init__(self, output):
        self.output = output

    def compile(self, commands):
        return compile(commands)

    def execute(self, program):
        self.output.write(program)


def open_file(uri):
    uri_parts = urlparse(uri)
    output = open(uri_parts.path, 'w')

    return CommandListPrinter(output)
