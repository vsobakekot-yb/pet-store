import requests
from requests import Response


class HttpRequestClient:
    def __init__(self, base_url: str, timeout: int):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, endpoint: str, params=None) -> Response:
        url = self.base_url.rstrip('/') + '/' + endpoint.lstrip('/')

        response = self.session.get(
            url,
            timeout=self.timeout,
            params=params
        )

        return response

    def close(self):
        self.session.close()