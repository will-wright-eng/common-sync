# type: ignore[attr-defined]
"""sync common files accross github repos"""

import sys
from importlib import metadata as importlib_metadata

from .file_handler import FileHandler


def get_version() -> str:
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


__author__: str = "Will Wright"
__version__: str = get_version()
