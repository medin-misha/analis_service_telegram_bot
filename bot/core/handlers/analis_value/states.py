from aiogram.fsm.state import State, StatesGroup


class GetAnalisValue(StatesGroup):
    analis_id = State()
    date = State()
    value = State()


class GetAnalisId(StatesGroup):
    analis_id = State()


class DeleteAnalisId(StatesGroup):
    analis_id = State()
    analis_value_id = State()
