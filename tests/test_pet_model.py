import pytest
from pydantic import ValidationError

from models.pet_model import Pet
from tests.pet_data import make_pet_payload


def test_pet_creation():
    payload = make_pet_payload(1)

    pet = Pet(**payload)

    assert pet.id == payload['id']
    assert pet.name == payload['name']
    assert pet.status == payload['status']
    assert pet.photo_urls == payload['photoUrls']
    assert pet.category.id == payload['category']['id']
    assert pet.tags[0].id == payload['tags'][0]['id']


def test_pet_creation_without_category_and_tags():
    payload = make_pet_payload(1)
    payload.pop('category')
    payload.pop('tags')

    pet = Pet(**payload)
    assert pet.category is None
    assert pet.tags is None


def test_category_has_wrong_type():
    payload = make_pet_payload(1)
    payload['category'] = [{'id': 12,'name': 'Dogs'}]

    with pytest.raises(ValidationError) as err:
        Pet(**payload)

    assert err.value.errors()[0]['loc'] == ('category',)


def test_incorrect_nested_key():
    payload = make_pet_payload(10)
    payload['category']['id'] = '1'

    with pytest.raises(ValidationError) as err:
        Pet(**payload)
    assert err.value.errors()[0]['loc'] == ('category', 'id')


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


def test_photo_urls():
    payload = make_pet_payload(1)

    pet = Pet(**payload)

    assert pet.photo_urls == payload['photoUrls']


def test_dumping_pet_model():
    payload = make_pet_payload(1)
    payload['photo_urls'] = payload.pop('photoUrls')

    pet = Pet(**payload)

    dump = pet.model_dump(by_alias=True)

    assert 'photoUrls' in dump
    assert 'photo_urls' not in dump
    assert dump['photoUrls'] == payload['photo_urls']
