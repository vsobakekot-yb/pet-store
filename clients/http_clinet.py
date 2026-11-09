import requests
from requests import Response

from types import TracebackType


class HttpRequestClient:
    def __init__(self, base_url: str, timeout: int):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()


    def __enter__(self):
        return self


    def _build_url(self, endpoint):
        return self.base_url.rstrip('/') + '/' + endpoint.lstrip('/')


    def get(self, endpoint: str, params=None) -> Response:
        url = self._build_url(endpoint)

        response = self.session.get(
            url,
            timeout=self.timeout,
            params=params
        )

        return response


    def delete(self, endpoint: str, params=None):
        url = self._build_url(endpoint)

        response = self.session.delete(
            url,
            timeout=self.timeout,
            params=params
        )
        return response


    def post(self, endpoint: str, json: dict) -> Response:
        url = self._build_url(endpoint)

        response = self.session.post(
            url=url,
            json=json,
            timeout=self.timeout
        )
        return response


    def put(self, endpoint: str, json:dict) -> Response:
        url = self._build_url(endpoint)

        response = self.session.put(
            url=url,
            json=json,
            timeout=self.timeout
        )
        return response


    def close(self):
        self.session.close()


    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:
        self.close()
