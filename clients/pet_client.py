from clients.http_clinet import HttpRequestClient


class PetClient:
    def __init__(self, client:HttpRequestClient):
        self._client = client


    def create_pet(self,payload: dict):
        return self._client.post(
            'pet',
            payload
        )


    def get_pet(self, pet_id: int):
        return self._client.get(
            f'pet/{pet_id}'
        )

