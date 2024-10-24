from pydantic import BaseModel, PositiveInt
from annotated_types import Annotated, MaxLen, MinLen


class BaseUser(BaseModel):
    name: Annotated[str, MinLen(2), MaxLen(100)] = None
    age: PositiveInt = None
    weight: PositiveInt = None
    gender: bool = None


class CreateUser(BaseUser):
    pass


class ReturnUser(BaseUser):
    id: PositiveInt
