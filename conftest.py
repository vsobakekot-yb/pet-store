import pytest
import secrets

from clients.http_clinet import HttpRequestClient
from clients.pet_client import PetClient


@pytest.fixture(scope="function")
def http_client():
    client = HttpRequestClient(
        'https://petstore3.swagger.io/api/v3',
        timeout=10
    )
    yield client
    client.close()


@pytest.fixture(scope='function')
def offline_http_client():
    client = HttpRequestClient(
        'https://example.com/',
        timeout=5
    )
    yield client
    client.close()


@pytest.fixture(scope='function')
def pet_client(http_client):
    return PetClient(http_client)



@pytest.fixture(scope='function')
def created_pet(pet_client):
    pet_id = secrets.randbelow(2 ** 63 - 1) + 1
    payload = {
        "id": pet_id,
        "name": "Buddy",
        "category": {
            "id": 1,
            "name": "Dogs"
        },
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": "available"
    }
    response = pet_client.create_pet(
        payload
    )
    assert response.status_code == 200
    assert response.json()['id'] == pet_id
    yield payload

    response = pet_client.delete_pet(pet_id)
    assert response.status_code == 200

    assert pet_client.get_pet(pet_id).status_code == 404
