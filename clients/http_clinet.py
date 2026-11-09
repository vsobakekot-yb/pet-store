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


    def _request(self, method: str, endpoint: str, **kwargs) -> Response:
        kwargs.setdefault('timeout', self.timeout)

        return self.session.request(method, self._build_url(endpoint), **kwargs)


    def _build_url(self, endpoint):
        return self.base_url.rstrip('/') + '/' + endpoint.lstrip('/')


    def get(self, endpoint: str, params=None) -> Response:
        return self._request('GET', endpoint, params=params)


    def delete(self, endpoint: str, params=None):
        return self._request('DELETE', endpoint, params=params)


    def post(self, endpoint: str, json: dict) -> Response:
        return self._request('POST', endpoint, json=json)


    def put(self, endpoint: str, json:dict) -> Response:
        return self._request('PUT', endpoint, json=json)


    def close(self):
        self.session.close()


    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:
        self.close()
