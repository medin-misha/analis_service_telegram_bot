from pydantic import BaseModel, PositiveInt


class BaseAnalis(BaseModel):
    name: str
    unit: str


class ReturnAnalis(BaseAnalis):
    id: PositiveInt


class CreateAnalis(BaseAnalis):
    user_name: str = None


class CreateAnalisModel(BaseAnalis):
    user_id: PositiveInt
