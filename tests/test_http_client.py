from unittest.mock import Mock

import pytest
import requests

from clients.http_clinet import HttpRequestClient


def test_get_forwards_arguments_to_session(offline_http_client,monkeypatch):
    mock_get = Mock()

    endpoint = '/users'
    query_params = {'status': 'active'}

    monkeypatch.setattr(offline_http_client.session, 'request', mock_get)

    offline_http_client.get(endpoint=endpoint, params=query_params)

    mock_get.assert_called_once_with(
        "GET",
        "https://example.com/users",
        params=query_params,
        timeout=5,
    )


def test_post_forwards_arguments_to_session(offline_http_client,monkeypatch):
    mock_post = Mock()

    payload = {"test": 'message'}
    endpoint = '/pet'

    monkeypatch.setattr(offline_http_client.session, 'request', mock_post)

    offline_http_client.post(endpoint=endpoint,json=payload)

    mock_post.assert_called_once_with(
        "POST",
        "https://example.com/pet",
        json=payload,
        timeout=5,
    )


def test_delete_forwards_arguments_to_session(offline_http_client, monkeypatch):
    expected_response = requests.Response()

    mock_delete = Mock(return_value=expected_response)
    endpoint = '/pet'
    params = {'some': 'params'}

    monkeypatch.setattr(offline_http_client.session, 'request', mock_delete)

    actual_response = offline_http_client.delete(endpoint=endpoint, params=params)

    mock_delete.assert_called_once_with(
        "DELETE",
        "https://example.com/pet",
        params=params,
        timeout=5,
    )
    assert expected_response is actual_response


def test_put_forwards_arguments_to_session(offline_http_client, monkeypatch):
    expected_response = requests.Response()

    mock_put = Mock(return_value=expected_response)
    endpoint = '/pet'
    payload = {'test': 'update'}

    monkeypatch.setattr(offline_http_client.session, 'request', mock_put)

    actual_response = offline_http_client.put(endpoint, payload)

    mock_put.assert_called_once_with(
        "PUT",
        "https://example.com/pet",
        json=payload,
        timeout=5,
    )
    assert actual_response is expected_response


def test_network_error(offline_http_client, monkeypatch):
    mock_get = Mock(side_effect=requests.Timeout)

    endpoint = '/users'
    query_params = {'status': 'active'}

    monkeypatch.setattr(offline_http_client.session, 'request', mock_get)

    with pytest.raises(requests.Timeout):
        offline_http_client.get(endpoint, params=query_params)

    mock_get.assert_called_once_with(
        "GET",
        "https://example.com/users",
        params=query_params,
        timeout=5,
    )


def test_503_error_from_get(offline_http_client, monkeypatch):
    expected_response = requests.Response()
    expected_response.status_code = 503

    mock = Mock(return_value=expected_response)


    endpoint = '/users'
    query_params = {'status': 'active'}

    monkeypatch.setattr(offline_http_client.session, 'request',  mock)

    actual_response = offline_http_client.get(endpoint, query_params)

    mock.assert_called_once_with(
        "GET",
        "https://example.com/users",
        params=query_params,
        timeout=5,
    )
    assert actual_response is expected_response
    assert actual_response.status_code == 503


def test_env_for_http_client(monkeypatch, request):
    monkeypatch.setenv('PETSTORE_BASE_URL', 'https://test.example.com')
    client = request.getfixturevalue('http_client')

    assert client.base_url == 'https://test.example.com'


def test_enter_returns_same_object():
    client = HttpRequestClient('https://petstore3.swagger.io/api/v3', timeout=10)

    with client as cli:
        assert cli is client


def test_session_close_called_once(monkeypatch):
    cli = HttpRequestClient('https://petstore3.swagger.io/api/v3', timeout=10)
    mock = Mock()
    monkeypatch.setattr(cli.session, 'close', mock)

    with cli:
        pass

    mock.assert_called_once_with()


def test_exit_calls_during_the_exception(monkeypatch):
    cli = HttpRequestClient('https://petstore3.swagger.io/api/v3', timeout=10)
    mock = Mock()

    monkeypatch.setattr(cli.session, 'close', mock)
    expected_error = requests.HTTPError('Expected error')

    with pytest.raises(requests.HTTPError) as exc:
        with cli:
            raise expected_error

    mock.assert_called_once_with()
    assert exc.value is expected_error
