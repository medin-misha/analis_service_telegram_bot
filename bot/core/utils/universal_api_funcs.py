import requests
from typing import List, Any
from ..config import settings


class UniversalApiFuncs:
    """
    базовый класс обращения к API для того что бы он заработал нужно в init аргументом suffix передать одно из значений
        /users/, /analis/, analis/value
    """

    def __init__(self, suffix: str):
        self.url: str = settings.server + suffix

    def _return_response(self, response) -> Any:
        if response.status_code == 200:
            return response.json()
        elif response.status_code != 200:
            return response.status_code
        return None

    def create(self, model_data: dict) -> dict | None:
        response = requests.post(url=self.url, json=model_data)
        return self._return_response(response=response)

    def get_all(self) -> List[dict]:
        response = requests.get(url=self.url)
        return self._return_response(response=response)

    def get_by_id(self, id: int) -> dict | None | int:
        response = requests.get(url=self.url + str(id))
        return self._return_response(response=response)

    def get_by_name(self, name: str) -> dict | None | int:
        response = requests.get(url=self.url + "name/" + name)
        return self._return_response(response=response)

    def patch_by_id(self, model_data: dict, id: int) -> dict | None | int:
        response = requests.patch(url=self.url + str(id), json=model_data)
        return self._return_response(response=response)

    def delete_by_id(self, id: int) -> int:
        response = requests.delete(url=self.url + str(id))
        return self._return_response(response=response)

    def schedule(self, user_id: int, analis_id: int):
        url = settings.server + "/schedule/"
        response = requests.post(
            url=url, json={"user_id": user_id, "analis_id": analis_id}
        )
        if response.status_code == 200:
            return response.content
        return _return_response(response=response)
