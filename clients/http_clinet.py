import requests
from requests import Response


class HttpRequestClient:
    def __init__(self, base_url: str, timeout: int):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

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


    def post(self, endpoint: str, json: dict) -> Response:
        url = self._build_url(endpoint)

        response = self.session.post(
            url=url,
            json=json,
            timeout=self.timeout
        )
        return response


    def close(self):
        self.session.close()
