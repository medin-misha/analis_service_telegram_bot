import requests
from typing import List
from core.config import settings
from core.utils import UniversalApiFuncs
from .validators import CreateAnalis, ReturnAnalis, CreateAnalisModel


class AnalisApiFuncs(UniversalApiFuncs):
    def __init__(self, suffix=None):
        suffix: str = "/analis/"
        self.url: str = settings.server + suffix

    def get_analis_by_user_name(self, user_name: str) -> List[ReturnAnalis] | None:
        user_api = UniversalApiFuncs("/users/")
        user = user_api.get_by_name(name=user_name)
        response = requests.get(self.url + f"user/{user.get("id")}")

        if response.status_code != 200:
            return
        return response.json()

    def get_analis_by_name_and_user_id(self, analis_name: str, user_id: int):
        response = requests.get(self.url + "/name/" + analis_name + f"/{user_id}")
        if response != 200:
            return
        return response.json()


def create_analis(analis_data: dict) -> ReturnAnalis:
    analis_api = AnalisApiFuncs()
    user_api = UniversalApiFuncs(suffix="/users/")
    user_id = user_api.get_by_name(name=analis_data.get("user_name")).get("id")

    analis_data.pop("user_name")
    analis_data["user_id"] = user_id

    analis_model_data: CreateAnalisModel = analis_data
    analis_return = analis_api.create(model_data=analis_model_data)
    return ReturnAnalis(**analis_return)


def get_analis_by_name_and_user(analis_name: str, user_name: str) -> ReturnAnalis:
    analis_api = AnalisApiFuncs()
    user_api = UniversalApiFuncs("/users/")
    user_id: int = user_api.get_by_name(name=name).get("id")
    return analis_api.get_analis_by_name_and_user_id(
        analis_name=analis_name, user_id=user_id
    )


def get_analis_by_user_name(user_name: str) -> List[ReturnAnalis]:
    analis_api = AnalisApiFuncs()
    return analis_api.get_analis_by_user_name(user_name=user_name)


def delete_analis_by_id(analis_id: int) -> int:
    analis_api = AnalisApiFuncs()
    return analis_api.delete_by_id(id=analis_id)
