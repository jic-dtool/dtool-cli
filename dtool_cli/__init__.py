"""dtool_cli module."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("dtool-cli")
except PackageNotFoundError:
    # Package is not installed.
    __version__ = "unknown"
