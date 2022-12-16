from importlib.metadata import version

_version = version("newertype")
__version__ = _version

from .newertype import NewerType
