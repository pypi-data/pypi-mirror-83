import copy
import os
from requests import Session


class Client:
    def __init__(self, version: str = "2.0"):
        self.version = version
        self.host = os.getenv(f"DBC_HOST", None)
        self.token = os.getenv(f"DBC_TOKEN", None)
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.session = Session()

    @property
    def url(self):
        return f"https://{self.host}/api/{self.version}"

    def call(self, method, endpoint, params=None, json=None, headers=None, **kwargs):
        if headers is None:
            headers = self.headers
        else:
            tmp_headers = copy.deepcopy(self.headers)
            tmp_headers.update(headers)
            headers = tmp_headers
        return self.session.request(
            method,
            self.url + endpoint,
            params=params,
            json=json,
            headers=headers,
            **kwargs,
        )
