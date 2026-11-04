def make_pet_payload(pet_id: int):
    payload = {
        "id": pet_id,
        "name": 'Monty',
        'category': {
            "id": 4,
            "name": 'Dogs'
        },
        "status": 'available',
        "photoUrls": ['/photo1', '/photo2'],
        'tags': [
            {
                "id": 1,
                'name': 'tag_1'
            }
        ]
    }
    return payload