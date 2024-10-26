from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from .utils import (
    create_analis,
    get_analis_by_name_and_user,
    get_analis_by_user_name,
    delete_analis_by_id,
)
from .validators import CreateAnalis, ReturnAnalis
from .messages import text
from .states import GetAnalisData, DeleteAnalis
from .keyboards import get_analis_keyboard

router = Router()


@router.message(Command("get_analis"))
async def get_analis(msg: Message):
    analis_list: ReturnAnalis = get_analis_by_user_name(
        user_name=msg.from_user.username
    )
    if analis_list is None:
        await msg.answer(text=text.get("no_analis"), reply_markup=get_analis_keyboard())
    else:
        message = text.get("get_analis_list")
        for one_analis in analis_list:
            message += text.get("get_analis_list_elem").format(
                id=one_analis.get("id"),
                name=one_analis.get("name"),
                unit=one_analis.get("unit"),
            )
        await msg.answer(text=message, reply_markup=get_analis_keyboard())


# Create analis handlers
@router.message(Command("create_analis"))
async def create_analis_handler(msg: Message, state: FSMContext):
    await msg.answer(text=text.get("create_analis"))
    await state.set_state(GetAnalisData.name)


@router.message(F.text, GetAnalisData.name)
async def set_name_in_analis(msg: Message, state: FSMContext):
    await state.set_data({"name": msg.text})
    await msg.answer(text=text.get("get_unit"))
    await state.set_state(GetAnalisData.unit)


@router.message(F.text, GetAnalisData.unit)
async def set_unit_in_analis(msg: Message, state: FSMContext):
    analis_data: dict = await state.get_data()
    analis_data["unit"] = msg.text
    analis_data["user_name"] = msg.from_user.username
    analis: ReturnAnalis = create_analis(analis_data=analis_data)
    message = text.get("get_analis_list_elem").format(
        id=analis.id, name=analis.name, unit=analis.unit
    )
    await msg.answer(text="Создан анализ:\n\n" + message)
    await state.clear()

# Delete analid handler
@router.message(Command("delete_analis"))
async def delete_analis_by_id_handler(msg: Message, state: FSMContext):
    await msg.answer(text=text.get("delete_analis"))
    await state.set_state(DeleteAnalis.id)

@router.message(F.text, DeleteAnalis.id)
async def get_id(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer(text=text.get("delete_id_fail"))
        await state.set_state(DeleteAnalis.id)
    else:
        delete_analis_by_id(analis_id=int(msg.text))
        await msg.answer(text=text.get("delete_analis_successful"), reply_markup=get_analis_keyboard())
        await state.clear()