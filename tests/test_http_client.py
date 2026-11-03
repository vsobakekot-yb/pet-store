from unittest.mock import Mock

import pytest
import requests


def test_get_forwards_arguments_to_session(offline_http_client,monkeypatch):
    mock_get = Mock()

    endpoint = '/users'
    query_params = {'status': 'active'}

    monkeypatch.setattr(offline_http_client.session, 'get', mock_get)

    offline_http_client.get(endpoint=endpoint, params=query_params)

    mock_get.assert_called_once_with(
        'https://example.com/users',
        timeout=5,
        params=query_params,
    )


def test_post_forwards_arguments_to_session(offline_http_client,monkeypatch):
    mock_post = Mock()

    _json = {"test": 'message'}
    endpoint = '/pet'

    monkeypatch.setattr(offline_http_client.session, 'post', mock_post)

    offline_http_client.post(endpoint=endpoint,json=_json)

    mock_post.assert_called_once_with(
        url='https://example.com/pet',
        json=_json,
        timeout=5
    )

def test_network_error(offline_http_client, monkeypatch):
    mock_get = Mock(side_effect=requests.Timeout)

    endpoint = '/users'
    query_params = {'status': 'active'}

    monkeypatch.setattr(offline_http_client.session, 'get', mock_get)

    with pytest.raises(requests.Timeout):
        offline_http_client.get(endpoint, params=query_params)

    mock_get.assert_called_once_with(
        'https://example.com/users',
        timeout=5,
        params=query_params,
    )


def test_503_error_from_get(offline_http_client, monkeypatch):
    expected_response = requests.Response()
    expected_response.status_code = 503

    mock = Mock(return_value=expected_response)


    endpoint = '/users'
    query_params = {'status': 'active'}

    monkeypatch.setattr(offline_http_client.session, 'get',  mock)

    actual_response = offline_http_client.get(endpoint, query_params)

    mock.assert_called_once_with(
        'https://example.com/users',
        timeout=5,
        params=query_params
    )
    assert actual_response is expected_response
    assert actual_response.status_code == 503


