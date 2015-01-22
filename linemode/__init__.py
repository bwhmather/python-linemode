from urllib.parse import urlparse

from linemode.drivers import star, command_list
from linemode.spooler import PrintSpooler
from linemode.exceptions import NotSupportedError


_BUILTIN_DRIVERS = {
    'star+tcp': star.open_tcp,
    'star+lpt': star.open_lpt,
    'star+com': star.open_com,
    'star+stdout': star.open_debug,

    'commands+file': command_list.open_file,
    'commands+stdout': command_list.open_stdout,
}

_drivers = {}
_drivers.update(_BUILTIN_DRIVERS)


def register_driver(uri_scheme, factory):
    _drivers[uri_scheme] = factory


def open_printer(uri):
    scheme = urlparse(uri).scheme
    if not scheme or scheme == uri:
        raise ValueError("Malformed printer uri")
    try:
        driver = _drivers[scheme]
    except KeyError:
        raise NotSupportedError("Unrecognised printer uri")
    else:
        return driver(uri)

__all__ = ['register_driver', 'open_printer', 'PrintSpooler']
