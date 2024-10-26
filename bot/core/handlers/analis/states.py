from aiogram.fsm.state import State, StatesGroup


class GetAnalisData(StatesGroup):
    name = State()
    unit = State()

class DeleteAnalis(StatesGroup):
    id = State()