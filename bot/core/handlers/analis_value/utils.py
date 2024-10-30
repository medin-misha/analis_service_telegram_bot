import requests
from datetime import datetime
from typing import List
from io import BytesIO

from core import settings
from core.utils import UniversalApiFuncs
from .validators import ReturnAnalisValue, CreateAnalisValue


class AnalisApiFuncs(UniversalApiFuncs):
    def __init__(self, suffix=None):
        suffix: str = "/analis/"
        self.url: str = settings.server + suffix

    def get_analis_ids_by_user_name(self, user_name: str) -> List[int] | None:
        user_api = UniversalApiFuncs("/users/")
        user = user_api.get_by_name(name=user_name)
        response = requests.get(self.url + f"user/{user.get("id")}")

        if response.status_code != 200:
            return

        ids_list: list = []
        for analis in response.json():
            ids_list.append(analis.get("id"))
        return ids_list

    def get_analis_list_by_user_name(self, user_name: str) -> List[dict] | None:
        user_api = UniversalApiFuncs(suffix="/users/")
        user = user_api.get_by_name(name=user_name)
        user_analis_list_response = requests.get(
            url=self.url + f"user/{user.get('id')}"
        )

        return (
            user_analis_list_response.json()
            if user_analis_list_response.status_code == 200
            else None
        )


class AnalisValueApiFuncs(UniversalApiFuncs):
    def __init__(self, suffix=None):
        suffix: str = "/analis/value/"
        self.url: str = settings.server + suffix

    def get_analis_values_by_analis_id(self, id: int) -> List[dict] | None:
        response = requests.get(url=self.url + f"analis/{id}")
        return response.json() if response.status_code == 200 else None

    def get_analis_values_ids_by_analis_id(self, analis_id: int) -> List[int] | None:
        analis_values = self.get_analis_values_by_analis_id(analis_id)
        if isinstance(analis_values, int):
            return

        ids_list: list = []
        for value in analis_values:
            ids_list.append(value.get("id"))
        return ids_list


def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_user_analises(user_name: str) -> List[dict] | None:
    return AnalisApiFuncs().get_analis_list_by_user_name(user_name=user_name)


def get_analis_values_by_analis_id(id: int) -> List[ReturnAnalisValue]:
    analis_value_api = AnalisValueApiFuncs()
    analis_values = analis_value_api.get_analis_values_by_analis_id(id=id)
    if analis_values is None:
        return
    else:
        analis_value_models = [
            ReturnAnalisValue(**analis_value) for analis_value in analis_values
        ]
        return analis_value_models


def check_existence_analis(id: int, user_name: str) -> bool:
    analis_api = AnalisApiFuncs()
    ids = analis_api.get_analis_ids_by_user_name(user_name=user_name)
    return True if id in ids else False


def create_analis_value(
    analis_value_data: dict, user_name: str
) -> ReturnAnalisValue | int:
    user_api = UniversalApiFuncs(suffix="/users/")
    analis_value_api = UniversalApiFuncs("/analis/value/")

    analis_value_data["user_id"] = user_api.get_by_name(name=user_name).get("id")
    analis_value_model_data: CreateAnalisValue = analis_value_data

    analis_value_model = analis_value_api.create(model_data=analis_value_model_data)

    return (
        ReturnAnalisValue(**analis_value_model)
        if not isinstance(analis_value_model, int)
        else analis_value_model
    )


def delete_analis_value(value_id: int, analis_id: id) -> int:
    analis_value_api = AnalisValueApiFuncs()
    analis_values = analis_value_api.get_analis_values_ids_by_analis_id(
        analis_id=analis_id
    )
    if value_id in analis_values:
        return analis_value_api.delete_by_id(id=value_id)
    else:
        return 404


def get_statistic_image(analis_id: int, user_name: str):
    user_api = UniversalApiFuncs("/users/")
    user = user_api.get_by_name(name=user_name)
    image = user_api.schedule(user_id=user.get("id"), analis_id=analis_id)
    if isinstance(image, int):
        return
    return image
