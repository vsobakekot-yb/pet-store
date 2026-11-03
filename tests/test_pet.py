import secrets

import pytest
import resource

import requests
from pydantic import ValidationError
from requests import Response

from clients.http_clinet import HttpRequestClient
from models.pet_model import Pet

@pytest.mark.parametrize('status', ['available', 'sold', 'pending'])
def test_find_by_status(pet_client, status):

    response = pet_client.find_by_status(status)

    assert response.status_code == 200

    pets = response.json()
    assert isinstance(pets, list)

    for pet in pets:
        assert pet['status'] == status


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

@pytest.mark.parametrize(
    'pet_id, name, status, photoUrls, remove_urls, expected_field',
    [
        ('22', 'billy', 'available', ['/photo1', '/photo2'], False, 'id'),
        (22, 'billy', 'ololo', ['/photo1', '/photo2'], False, 'status'),
        (22, 'billy', 'available',['/photo1', '/photo2'], True, 'photoUrls')
    ]
)
def test_incorrect_pet(pet_id,name,status, photoUrls,remove_urls,expected_field):
    payload = {
        "id": pet_id,
        "name": name,
        "status": status,
        "photoUrls": photoUrls
    }
    if remove_urls:
        payload.pop('photoUrls')

    with pytest.raises(ValidationError) as exc_info:
        Pet(**payload)

    assert (expected_field,) in [
        error['loc'] for error in exc_info.value.errors()
    ]


def test_create_and_validate_pet(pet_client,created_pet):
    pet = created_pet

    response = pet_client.get_pet(pet['id'])
    assert  response.status_code == 200

    actual_pet = Pet(**response.json())

    assert actual_pet.id == pet['id']
    assert actual_pet.name == pet['name']
    assert actual_pet.status == pet['status']


@pytest.mark.parametrize('status', ['available', 'sold', 'pending'])
def test_different_statuses(status, pet_client, created_pet):
    pet = created_pet

    response = pet_client.get_pet(pet['id'])
    assert response.status_code == 200

    pet['status'] = status
    response = pet_client.update_pet(pet)
    assert response.status_code == 200

    response = pet_client.get_pet(pet['id'])
    assert response.status_code == 200

    updated_pet = Pet.model_validate(response.json())

    assert updated_pet.status == status
    assert updated_pet.name == pet['name']
    assert updated_pet.id == pet['id']


def test_get_non_existent_pet(pet_client):
    response = pet_client.get_pet(secrets.randbelow(2 ** 63 - 1) + 1)
    assert response.status_code == 404


def test_get_response_mock(monkeypatch):
    def mock_session_get(session, url, timeout, params=None, **kwargs):
        response = Response()
        response.status_code = 200

        response._mocked_url = url
        response._mocked_timeout = timeout
        response._mocked_params = params

        return response


    monkeypatch.setattr(requests.Session, 'get', mock_session_get)
    base_url = 'https://example.com/'
    client = HttpRequestClient(base_url=base_url, timeout=5)

    endpoint = '/users'
    query_params = {'status': 'active'}
    response = client.get(endpoint=endpoint, params=query_params)

    assert response._mocked_url == 'https://example.com/users'
    assert response._mocked_params == {'status': 'active'}
    assert response._mocked_timeout == 5

    client.close()








