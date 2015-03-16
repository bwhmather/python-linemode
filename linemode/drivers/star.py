import sys
from urllib.parse import urlparse

from linemode.base import Printer


class StarPrinterCompiler(object):
    def __init__(self):
        # TODO check that ascii is a subset of all the other charsets
        self._charset = 'ascii'

        self.COMMANDS = {
            'reset': b'\x18',
            'select-bold': b'\x1b\x45',
            'cancel-bold': b'\x1b\x46',
            'select-highlight': b'\x1b\x34',
            'cancel-highlight': b'\x1b\x35',
            'fontsize-small': b'\x1b\x14',
            'fontsize-medium': b'\x1b\x0e',
            'fontsize-large': b'\x1b\x68\x32',
            'write': self._op_write_string,
            'barcode': self._op_barcode,
            'newline': b'\n',
            'cut-through': b'\x1b\x64\x02',
            'cut-partial': b'\x1b\x64\x03',
            'cut-through-immediate': b'\x1b\x64\x00',
            'cut-partial-immediate': b'\x1b\x64\x01',
        }
        self.CHARSET_CODES = {
            'ascii': b'\x00',  # TODO Normal is not ascii but something weird
            'euc_jp': b'\x02',  # TODO Katakana
            'cp437': b'\x03',
            'cp858': b'\x04',
            'cp852': b'\x05',
            'cp860': b'\x06',
            'cp861': b'\x07',
            'cp863': b'\x08',
            'cp865': b'\x09',
            'cp866': b'\x0a',
            'cp855': b'\x0b',
            'cp857': b'\x0c',
            'cp862': b'\x0d',
            'cp864': b'\x0e',
            'cp737': b'\x0f',
            'cp851': b'\x10',
            'cp869': b'\x11',
            'cp928': b'\x12',  # TODO not supported by python
            'cp772': b'\x13',  # TODO not supported by python
            'cp774': b'\x14',  # TODO not supported by python
            'cp874': b'\x15',
            'cp1252': b'\x20',
            'cp1250': b'\x21',
            'cp1251': b'\x22',
            'cp3840': b'\x40',  # TODO not supported by python
            'cp3841': b'\x41',  # TODO not supported by python
            'cp3843': b'\x42',  # TODO not supported by python
            'cp3844': b'\x43',  # TODO not supported by python
            'cp3845': b'\x44',  # TODO not supported by python
            'cp3846': b'\x45',  # TODO not supported by python
            'cp3847': b'\x46',  # TODO not supported by python
            'cp3848': b'\x47',  # TODO not supported by python
            'cp1001': b'\x48',  # TODO not supported by python
            'cp2001': b'\x49',  # TODO not supported by python
            'cp3001': b'\x4a',  # TODO not supported by python
            'cp3002': b'\x4b',  # TODO not supported by python
            'cp3011': b'\x4c',  # TODO not supported by python
            'cp3012': b'\x4d',  # TODO not supported by python
            'cp3021': b'\x4e',  # TODO not supported by python
            'cp3041': b'\x4f',  # TODO not supported by python
        }

    def _op_write_string(self, string):
        try:
            return string.encode(self._charset)
        except UnicodeEncodeError:
            # could not encode string using current charset
            # conduct a brute force search
            for charset in self.CHARSET_CODES:
                try:
                    return (
                        b'\x1b\x1d\x74' +
                        self.CHARSET_CODES[charset] +
                        string.encode(charset)
                    )
                except UnicodeEncodeError:
                    # unknown character in charset
                    continue
                except LookupError:
                    # charset not supported by python
                    continue
                else:
                    self._charset = charset
            # TODO should this be an error
            return string.encode(self._charset, errors='replace')

    def _op_barcode(self, style, data):
        if style != 'qr':
            raise ValueError('unsupported barcode format', style)

        # TODO make configurable
        # TODO figure out what this stuff actually means!
        return (
            b'\x1b\x1d\x52\x7f\x00\x1b\x1d\x79\x53\x30\x01\x1b\x1d\x79\x53' +
            b'\x31\x02\x1b\x1d\x79\x53\x32\x08\x1b\x1d\x79\x44\x31\x00' +
            bytes([len(data)]) +
            b'\x00' +
            bytes(data) +
            b'\x1b\x1d\x79\x50'
        )

    def _compile_command(self, command):
        if isinstance(command, str):
            command_name, args = command, []
        else:
            command_name, *args = command

        command = self.COMMANDS[command_name]
        if isinstance(command, bytes):
            if len(args):
                raise TypeError("%s takes no arguments" % command_name)
            return command
        return command(*args)

    def __call__(self, commands):
        return b''.join(
            self._compile_command(command) for command in commands
        )


class StarPrinter(Printer):
    compiler = StarPrinterCompiler

    def __init__(self, port, *, _close_port=False):
        super(StarPrinter, self).__init__()

        self._port = port
        self._close_port = _close_port

    def compile(self, commands):
        return self.compiler()(commands)

    def execute(self, program):
        self._port.write(program)
        self._port.flush()

    def shutdown(self):
        if self._close_port:
            self._port.close()


def open_tcp(uri):
    raise NotImplementedError()


def open_lpt(uri):
    uri_parts = urlparse(uri)
    port = open(uri_parts.path, 'r+b')

    return StarPrinter(port, _close_port=True)


def open_com(uri):
    import serial

    uri_parts = urlparse(uri)
    port = serial.Serial(uri_parts.netloc)

    return StarPrinter(port, _close_port=True)


def open_stdout(uri):
    return StarPrinter(sys.stdout)


def open_debug(uri):
    class DebugPort(object):
        def write(self, data):
            for line in data.split(b'\n'):
                print(repr(line))

        def flush(self):
            pass

    return StarPrinter(DebugPort())
