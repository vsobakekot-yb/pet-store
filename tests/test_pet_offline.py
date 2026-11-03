from unittest.mock import Mock

import requests

from clients.pet_client import PetClient
from conftest import http_client


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
    http_client.get.assert_called_once_with('pet/findByStatus',params={'status':'available'})
    assert actual_response is expected_response


def test_create_pet_offline():
    expected_response = requests.Response()
    http_client = Mock()
    http_client.post.return_value = expected_response

    pet_client = PetClient(http_client)
    payload = {'test': 'value'}

    actual_response = pet_client.create_pet(
        payload
    )
    http_client.post.assert_called_once_with('pet', payload)
    assert actual_response is expected_response


def test_put_offline():
    expected_response = requests.Response()
    http_client = Mock()
    http_client.put.return_value = expected_response

    pet_client = PetClient(http_client)
    payload = {'test': 'value'}

    actual_response = pet_client.update_pet(
        payload
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