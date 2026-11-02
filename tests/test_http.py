import secrets

import pytest
from pydantic import ValidationError

from models.pet_model import Pet

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


def test_created_pet_can_be_retrieved(pet_client, created_pet):
    expected_pet = created_pet

    response = pet_client.get_pet(expected_pet['id'])
    assert response.status_code == 200

    actual_pet = response.json()
    assert actual_pet['id'] == expected_pet['id']
    assert actual_pet['name'] == expected_pet['name']


def test_delete_nonexistent_pet(pet_client):
    uid = secrets.randbelow(2 ** 63 - 1) + 1
    response = pet_client.get_pet(uid)
    assert response.status_code == 404

    response = pet_client.delete_pet(uid)

    assert response.status_code == 200

    response = pet_client.delete_pet(uid)
    assert response.status_code == 200

    assert pet_client.get_pet(uid).status_code == 404


def test_change_pet_name(pet_client, created_pet):
    pet = created_pet

    response = pet_client.get_pet(pet['id'])
    assert response.status_code == 200

    pet['name'], pet['status'] = 'Max', 'sold'

    response = pet_client.update_pet(pet)
    assert response.status_code == 200

    updated_pet = response.json()
    assert updated_pet['name'] == 'Max'
    assert updated_pet['status'] == 'sold'

    response = pet_client.get_pet(pet['id'])

    result = response.json()
    assert result['name'] == 'Max'
    assert result['status'] == 'sold'


def test_incorrect_pet():
    payload = {
        "id": "wrong_id",
        "name": "Buddy",
        "status": "available",
        "photoUrls": []
    }
    with pytest.raises(ValidationError):
        Pet(**payload)


def test_create_and_validate_pet(pet_client,created_pet):
    pet = created_pet

    response = pet_client.get_pet(pet['id'])
    assert  response.status_code == 200

    actual_pet = Pet(**response.json())

    assert actual_pet.id == pet['id']
    assert actual_pet.name == pet['name']
    assert actual_pet.status == pet['status']

