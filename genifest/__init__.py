"""Top-level package for genifest."""
import os

from dotenv import load_dotenv

__author__ = """Torsten Irländer"""
__email__ = "torsten.irlaender@googlemail.com"
__version__ = "0.1"

load_dotenv()  # take environment variables from .env.


def get_package_root() -> str:  # pragma: no cover
    """
    Returns path to the root folder of genifest
    package.
    """
    return os.path.dirname(os.path.abspath(__file__))


PACKAGE_PATH = get_package_root()
PACKAGE_VERSION = __version__
