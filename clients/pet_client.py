from requests import Response

from clients.http_clinet import HttpRequestClient


class PetClient:
    def __init__(self, client:HttpRequestClient) -> None:
        self._client = client


    def create_pet(self,payload: dict) -> Response:
        return self._client.post(
            'pet',
            payload
        )

    def delete_pet(self, pet_id: int) -> Response:
        return self._client.delete(
            f'pet/{pet_id}'
        )


    def get_pet(self, pet_id: int) -> Response:
        return self._client.get(
            f'pet/{pet_id}'
        )

    def find_by_status(self, status: str) -> Response:
        return self._client.get(
            f'pet/findByStatus',
            params={'status': status}
        )

    def update_pet(self, payload:dict) -> Response:
        return self._client.put(
            'pet',
            payload
        )

