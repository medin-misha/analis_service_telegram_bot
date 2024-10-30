from pydantic import BaseModel, PositiveInt
from datetime import date


class BaseAnalisValue(BaseModel):
    analis_id: PositiveInt
    user_id: PositiveInt
    date: date
    value: str


class CreateAnalisValue(BaseAnalisValue):
    pass


class ReturnAnalisValue(BaseAnalisValue):
    user_name: str = None
    analis_name: str = None
    id: PositiveInt
