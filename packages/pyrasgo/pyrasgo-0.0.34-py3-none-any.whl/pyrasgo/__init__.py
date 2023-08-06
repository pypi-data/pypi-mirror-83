__all__ = [
    'connect',
]

from pyrasgo.api import RasgoConnection


def connect(api_key):
    return RasgoConnection(api_key=api_key)