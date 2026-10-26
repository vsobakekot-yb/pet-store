import uuid
import secrets
from clients.pet_client import PetClient

def test_find_by_status(http_client):

    response = http_client.get(
        '/pet/findByStatus',
        {'status': 'available'}
    )

    pets = response.json()
    assert response.status_code == 200
    assert isinstance(pets, list)

    for pet in pets:
        assert pet['status'] == 'available'

def test_create_pet(http_client):
    payload = {
      "id": secrets.randbelow(2**63 - 1) + 1,
      "name": "doggie",
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
    response = http_client.post(
        'pet',
        payload
    )
    assert response.status_code == 200

    pet = response.json()

    assert pet['id'] == payload['id']
    assert pet['name'] == payload['name']


def test_pet_client(http_client):
    cli = PetClient(http_client)
    uid = secrets.randbelow(2**63 - 1) + 1

    payload = {
      "id": uid,
      "name": "doggie",
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

    response = cli.create_pet(
        payload
    )
    assert response.status_code == 200

    pet = cli.get_pet(uid).json()

    assert pet['id'] == uid
    assert pet['name'] == payload['name']

