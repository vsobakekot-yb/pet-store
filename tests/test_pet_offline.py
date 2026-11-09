from unittest.mock import Mock

import pytest
import requests

from clients.pet_client import PetClient
from models.pet_model import Pet
from tests.pet_data import make_pet_payload


@pytest.fixture(scope='function')
def http_client():
    return Mock()


def test_get_pet_offline():
    expected_response = requests.Response()
    http_client = Mock()
    http_client.get.return_value = expected_response

    pet_client = PetClient(http_client)

    actual_response = pet_client.get_pet(12)

    http_client.get.assert_called_once_with("pet/12")
    assert actual_response is expected_response


def test_find_by_status_offline():
    expected_response = requests.Response()
    http_client = Mock()
    http_client.get.return_value = expected_response

    pet_client = PetClient(http_client)

    actual_response = pet_client.find_by_status('available')
    http_client.get.assert_called_once_with(
        'pet/findByStatus',
        params={'status': 'available'}
    )
    assert actual_response is expected_response


def test_create_pet_offline():
    expected_response = requests.Response()
    http_client = Mock()
    http_client.post.return_value = expected_response

    payload = make_pet_payload(1)
    pet = Pet.model_validate(payload)

    pet_client = PetClient(http_client)

    actual_response = pet_client.create_pet(
        pet
    )
    http_client.post.assert_called_once_with('pet', payload)
    assert actual_response is expected_response


def test_update_pet_offline():
    expected_response = requests.Response()
    http_client = Mock()
    http_client.put.return_value = expected_response

    payload = make_pet_payload(1)
    pet = Pet.model_validate(payload)

    pet_client = PetClient(http_client)

    actual_response = pet_client.update_pet(
        pet
    )
    http_client.put.assert_called_once_with('pet', payload)
    assert actual_response is expected_response


def test_delete_pet_offline():
    expected_response = requests.Response()
    http_client = Mock()
    http_client.delete.return_value = expected_response

    pet_client = PetClient(http_client)

    actual_response = pet_client.delete_pet(12)
    http_client.delete.assert_called_once_with('pet/12')
    assert actual_response is expected_response


def test_created_pet_offline(http_client, request):
    response = Mock()
    response.status_code = 200
    response.json.return_value = {'id': -1}
    http_client.post.return_value = response

    http_client.delete.return_value = Mock(status_code=200)
    http_client.get.return_value = Mock(status_code=404)

    with pytest.raises(AssertionError):
        request.getfixturevalue('created_pet')

    payload = http_client.post.call_args.args[1]
    http_client.delete.assert_called_once_with(f'pet/{payload['id']}')
    http_client.get.assert_called_once_with(f'pet/{payload['id']}')







