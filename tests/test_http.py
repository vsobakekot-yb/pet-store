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
