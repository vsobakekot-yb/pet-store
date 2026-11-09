import secrets

import pytest

from models.pet_model import Pet

@pytest.mark.parametrize('status', ['available', 'sold', 'pending'])
def test_find_by_status(pet_client, status):

    response = pet_client.find_by_status(status)

    assert response.status_code == 200

    pets = response.json()
    assert isinstance(pets, list)

    for pet in pets:
        pet = Pet.model_validate(pet)
        assert pet.status == status


def test_created_pet_can_be_retrieved(pet_client, created_pet):
    expected_pet = created_pet

    response = pet_client.get_pet(expected_pet.id)
    assert response.status_code == 200

    actual_pet = Pet.model_validate(response.json())
    assert actual_pet.id == expected_pet.id
    assert actual_pet.id == expected_pet.name


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

    response = pet_client.get_pet(pet.id)
    assert response.status_code == 200

    pet.name, pet.status = 'Max', 'sold'

    response = pet_client.update_pet(pet)
    assert response.status_code == 200

    updated_pet = Pet.model_validate(response.json())
    assert updated_pet.name == 'Max'
    assert updated_pet.status == 'sold'

    response = pet_client.get_pet(pet.id)

    result = Pet.model_validate(response.json())
    assert result.name == 'Max'
    assert result.status == 'sold'


def test_create_and_validate_pet(pet_client,created_pet):
    pet = created_pet

    response = pet_client.get_pet(pet.id)
    assert  response.status_code == 200

    actual_pet = Pet.model_validate(response.json())

    assert actual_pet.id == pet.id
    assert actual_pet.name == pet.name
    assert actual_pet.status == pet.status


@pytest.mark.parametrize('status', ['available', 'sold', 'pending'])
def test_different_statuses(status, pet_client, created_pet):
    pet = created_pet

    response = pet_client.get_pet(pet.id)
    assert response.status_code == 200

    pet.status = status
    response = pet_client.update_pet(pet)
    assert response.status_code == 200

    response = pet_client.get_pet(pet.id)
    assert response.status_code == 200

    updated_pet = Pet.model_validate(response.json())

    assert updated_pet.status == status
    assert updated_pet.name == pet.name
    assert updated_pet.id == pet.id


def test_get_non_existent_pet(pet_client):
    response = pet_client.get_pet(secrets.randbelow(2 ** 63 - 1) + 1)
    assert response.status_code == 404






