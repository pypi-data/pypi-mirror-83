import pkgutil
import sys

__all__ = ["__version__", "version_info"]


__version__ = pkgutil.get_data(__package__, "VERSION").decode("ascii").strip()
version_info = tuple(int(v) if v.isdigit() else v for v in __version__.split("."))

if sys.version_info < (3, 6):
    sys.exit("os-aiohttp-utils %s requires Python 3.6+" % __version__)

del pkgutil
del sys
