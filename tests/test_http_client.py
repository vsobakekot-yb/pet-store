from unittest.mock import Mock

import pytest
import requests

from clients.http_clinet import HttpRequestClient


def test_get_forwards_arguments_to_session(monkeypatch):
    mock_get = Mock()

    base_url = 'https://example.com/'
    endpoint = '/users'
    query_params = {'status': 'active'}

    client = HttpRequestClient(base_url=base_url, timeout=5)
    monkeypatch.setattr(client.session, 'get', mock_get)

    client.get(endpoint=endpoint, params=query_params)

    mock_get.assert_called_once_with(
        'https://example.com/users',
        timeout=5,
        params=query_params,
    )

    client.close()


def test_post_forwards_arguments_to_session(monkeypatch):
    mock_post = Mock()

    base_url = 'https://example.com/'
    _json = {"test": 'message'}
    endpoint = '/pet'

    client = HttpRequestClient(base_url=base_url, timeout=5)
    monkeypatch.setattr(client.session, 'post', mock_post)

    client.post(endpoint=endpoint,json=_json)

    mock_post.assert_called_once_with(
        url='https://example.com/pet',
        json=_json,
        timeout=5
    )

    client.close()


def test_network_error(monkeypatch):
    mock_get = Mock(side_effect=requests.Timeout)

    base_url = 'https://example.com/'
    endpoint = '/users'
    query_params = {'status': 'active'}

    client = HttpRequestClient(base_url, timeout=1000)
    monkeypatch.setattr(client.session, 'get', mock_get)

    with pytest.raises(requests.Timeout):
        client.get(endpoint, params=query_params)

    mock_get.assert_called_once_with(
        'https://example.com/users',
        timeout=1000,
        params=query_params,
    )
    client.close()


def test_503_error_from_get(monkeypatch):
    expected_response = requests.Response()
    expected_response.status_code = 503

    mock = Mock(return_value=expected_response)


    base_url = 'https://example.com/'
    endpoint = '/users'
    query_params = {'status': 'active'}

    client = HttpRequestClient(base_url, timeout=5)
    monkeypatch.setattr(client.session, 'get',  mock)

    actual_response = client.get(endpoint, query_params)

    mock.assert_called_once_with(
        'https://example.com/users',
        timeout=5,
        params=query_params
    )
    assert actual_response is expected_response
    assert actual_response.status_code == 503


    client.close()


