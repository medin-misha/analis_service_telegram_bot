from pydantic import ValidationError
from core.utils import UniversalApiFuncs
from .validators import CreateUser, ReturnUser


def create_user(user_data: CreateUser) -> ReturnUser | int | None:
    api = UniversalApiFuncs(suffix="/users/")
    try:
        user_model: CreateUser = CreateUser(**user_data)
    except ValidationError:
        return

    return_user_data: ReturnUser = api.create(model_data=user_model.model_dump())
    return ReturnUser(**return_user_data)


def get_user_by_name(user_name: str) -> ReturnUser | int:
    api = UniversalApiFuncs(suffix="/users/")

    return_user_data: ReturnUser = api.get_by_name(name=user_name)
    return ReturnUser(**return_user_data)
