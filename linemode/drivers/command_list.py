import sys
from urllib.parse import urlparse

from linemode.base import Printer


def _compile_command(command):
    if isinstance(command, str):
        command_name, args = command, []
    else:
        command_name, *args = command

    if len(args):
        return (
            command_name + ": " +
            ", ".join(repr(arg) for arg in args)
        ).encode('utf-8')
    else:
        return command_name.encode('utf-8')


def compile(commands):
    return b'\n'.join(
        _compile_command(command) for command in commands
    )


class CommandListPrinter(Printer):
    def __init__(self, port):
        self._port = port

    def compile(self, commands):
        return compile(commands)

    def execute(self, program):
        self._port.write(program)

    def shutdown(self):
        self._port.close()


def open_file(uri):
    uri_parts = urlparse(uri)
    port = open(uri_parts.path, 'wb')

    return CommandListPrinter(port)


def open_stdout(uri):
    return CommandListPrinter(sys.stdout)
