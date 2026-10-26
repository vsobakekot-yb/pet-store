import uuid
import secrets

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
