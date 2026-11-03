from unittest.mock import Mock

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


