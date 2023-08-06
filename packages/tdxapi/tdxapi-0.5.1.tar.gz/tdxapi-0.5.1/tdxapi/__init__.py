import logging

from tdxapi.client import TdxClient  # noqa: F401

__version__ = "0.5.1"

logging.getLogger(__name__).addHandler(logging.NullHandler())
