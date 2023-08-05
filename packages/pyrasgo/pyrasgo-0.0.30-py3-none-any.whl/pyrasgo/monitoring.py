import os
import json
import logging
import requests
import functools

from pyrasgo.version import __version__ as pyrasgo_version

PRODUCTION_HEAP_KEY = '540300130'
STAGING_HEAP_KEY = '3353132567'

PRODUCTION = "PRODUCTION"
STAGING = "STAGING"
LOCAL = "LOCAL"
ENDPOINTS = {
    PRODUCTION: "api.rasgoml.com",
    LOCAL: "localhost"
}

HEAP_URL = "https://heapanalytics.com/api"
# props_api = f"{base_url}/add_user_properties"


def track_usage(func):
    @functools.wraps(func)
    def decorated(self, *args, **kwargs):
        from pyrasgo.connection import Connection
        if issubclass(self.__class__, Connection) or isinstance(self, Connection):
            self: Connection
            if self.environment == LOCAL:
                logging.info(f"Called {func.__name__} with parameters: {kwargs}")
            else:
                try:
                    track_call(
                        app_id=PRODUCTION_HEAP_KEY if self._hostname == ENDPOINTS[PRODUCTION] else STAGING_HEAP_KEY,
                        user_id=self._user_id,
                        event=func.__name__,
                        properties={"hostname": os.environ.get('RASGO_DOMAIN', ENDPOINTS[PRODUCTION]),
                                    "source": "pyrasgo",
                                    "class": self.__class__.__name__,
                                    "version": pyrasgo_version,
                                    "username": self._get_profile().get("username", "Unknown"),
                                    "input": args,
                                    **kwargs})
                except Exception:
                    logging.debug(f"Called {func.__name__} with parameters: {kwargs}")
        else:
            logging.debug(f"Cannot track functions called from {self.__class__.__name__} class.")
        return func(self, *args, **kwargs)
    return decorated


def track_call(app_id: str,
               user_id: int,
               event: str,
               properties: dict = None):
    """
    Send a "track" event to the Heap Analytics API server.

    :param event: event name
    :param properties: optional, additional event properties
    """
    data = {"app_id": app_id,
            "identity": user_id,
            "event": event}

    if properties is not None:
        data["properties"] = properties

    response = requests.post(url=f"{HEAP_URL}/track",
                             data=json.dumps(data),
                             headers={"Content-Type": "application/json"})
    response.raise_for_status()
    return response
