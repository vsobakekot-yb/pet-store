import pytest
from clients.http_clinet import HttpRequestClient


@pytest.fixture(scope="function")
def http_client():
    client = HttpRequestClient(
        'https://petstore3.swagger.io/api/v3',
        timeout=10
    )
    yield client
    client.close()
