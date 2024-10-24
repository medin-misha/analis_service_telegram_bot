from aiogram.fsm.state import State, StatesGroup


class GetUserData(StatesGroup):
    age = State()
    weight = State()
    gender = State()
