from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile, FSInputFile
from aiogram.fsm.context import FSMContext
from datetime import datetime
from typing import List

from .messages import text, now_date
from .states import GetAnalisValue, GetAnalisId, DeleteAnalisId
from .keyboards import (
    analis_value_date,
    commands_keyboard,
    analis_keyboard_builder,
    analises_not_found,
)
from .validators import ReturnAnalisValue
from .utils import (
    is_valid_date,
    create_analis_value,
    check_existence_analis,
    get_user_analises,
    get_analis_values_by_analis_id,
    get_statistic_image,
    delete_analis_value,
)


router = Router()


# Get analis value handler
@router.message(Command("analis_values"))
async def get_analis_list(msg: Message, state: FSMContext):
    await state.clear()
    analis_list: List[dict] = get_user_analises(user_name=msg.from_user.username)

    if analis_list is None:
        await msg.answer(
            text=text.get("analises_not_found"), reply_markup=analises_not_found()
        )
        await state.clear()
    else:
        message: str = ""

        for analis in analis_list:
            message += text.get("get_analis_list_elem").format(
                id=analis.get("id"), name=analis.get("name")
            )

        await msg.answer(
            text="Выбери ID значения какого анализа тебе нужы:\n" + message,
            reply_markup=analis_keyboard_builder(analises=analis_list),
        )
        await state.set_state(GetAnalisId.analis_id)


@router.message(F.text, GetAnalisId.analis_id)
async def return_analis_statistic_and_value(msg: Message, state: FSMContext):
    if not msg.text.isdigit:
        await state.set_state(GetAnalisId.analis_id)
        await msg.answer(text=text.get("get_analis_id_fail"))
    elif not check_existence_analis(id=int(msg.text), user_name=msg.from_user.username):
        await state.set_state(GetAnalisId.analis_id)
        await msg.answer(text=text.get("analis_not_found"))
    else:
        analis_values: List[ReturnAnalisValue] = get_analis_values_by_analis_id(
            id=int(msg.text)
        )
        if analis_values is not None:
            message = ""
            for value in analis_values:
                message += text.get("get_analis_value_elem").format(
                    id=value.id, value=value.value, date=value.date
                )
            image_statistic = get_statistic_image(
                analis_id=int(msg.text), user_name=msg.from_user.username
            )
            await msg.bot.send_photo(
                chat_id=msg.chat.id,
                photo=BufferedInputFile(image_statistic, filename="image.png"),
            )
            await msg.answer(
                text="Список анализов:\n\n" + message, reply_markup=commands_keyboard()
            )
            await state.clear()


# Create AnalisValue handlers
@router.message(Command("create_value"))
async def create_analis_value_handler(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(text=text.get("create_analis_value"))
    await state.set_state(GetAnalisValue.analis_id)


@router.message(F.text, GetAnalisValue.analis_id)
async def get_analis_id(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer(text=text.get("analis_id_fail"))
        await state.set_state(GetAnalisValue.analis_id)
    elif not check_existence_analis(id=int(msg.text), user_name=msg.from_user.username):
        await msg.answer(text=text.get("analis_not_found"))
        await state.set_state(GetAnalisValue.analis_id)
    else:
        analis_value_data: dict = {"analis_id": int(msg.text)}
        date = datetime.today().strftime("%Y-%m-%d")
        await state.set_data(analis_value_data)

        await msg.answer(
            text=text.get("get_analis_id_success").format(date=date),
            reply_markup=analis_value_date(),
        )
        await state.set_state(GetAnalisValue.date)


@router.message(F.text, GetAnalisValue.date)
async def get_analis_date(msg: Message, state: FSMContext):
    if msg.text == now_date:
        state_data = await state.get_data()
        state_data["date"] = datetime.today().strftime("%Y-%m-%d")
        await state.set_data(state_data)

        await msg.answer(text=text.get("get_analis_date_success"))
        await state.set_state(GetAnalisValue.value)

    elif is_valid_date(date_string=msg.text):
        state_data = await state.get_data()
        state_data["date"] = datetime.strptime(msg.text, "%Y-%m-%d").date().strftime("%Y-%m-%d")
        await state.set_data(state_data)

        await msg.answer(text=text.get("get_analis_date_success"))
        await state.set_state(GetAnalisValue.value)

    else:
        date = datetime.today().strftime("%Y-%m-%d")

        await msg.answer(text=text.get("get_analis_date_fail").format(date=date))
        await state.set_state(GetAnalisValue.date)


@router.message(F.text, GetAnalisValue.value)
async def get_analis_value(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer(text=text.get("get_analis_value_fail"))
        await state.set_state(GetAnalisValue.value)
    else:
        analis_value_data: dict = await state.get_data()
        analis_value_data["value"] = msg.text

        created_analis_value = create_analis_value(
            analis_value_data=analis_value_data, user_name=msg.from_user.username
        )
        await msg.answer(text=text.get("get_analis_value_success"))
        await msg.answer(
            text=text.get("get_analis_value_elem").format(
                id=created_analis_value.id,
                value=created_analis_value.value,
                date=created_analis_value.date,
            ),
            reply_markup=commands_keyboard(),
        )
        await state.clear()


# Delete analis Value handlers
@router.message(Command("delete_analis_value"))
async def delete_analis_value_handler(msg: Message, state: FSMContext):
    await state.clear()
    analis_list: List[dict] = get_user_analises(user_name=msg.from_user.username)

    if analis_list is None:
        await msg.answer(
            text=text.get("analises_not_found"), reply_markup=analises_not_found()
        )
        await state.clear()
    else:
        message: str = ""

        for analis in analis_list:
            message += text.get("get_analis_list_elem").format(
                id=analis.get("id"), name=analis.get("name")
            )

        await msg.answer(
            text="Выбери ID значения какого анализа тебе нужно удалить:\n" + message,
            reply_markup=analis_keyboard_builder(analises=analis_list),
        )
        await state.set_state(DeleteAnalisId.analis_id)


@router.message(F.text, DeleteAnalisId.analis_id)
async def get_analis_values_ids(msg: Message, state: FSMContext):
    if not msg.text.isdigit:
        await state.set_state(GetAnDeleteAnalisIdalisId.analis_id)
        await msg.answer(text=text.get("get_analis_id_fail"))
    elif not check_existence_analis(id=int(msg.text), user_name=msg.from_user.username):
        await state.set_state(DeleteAnalisId.analis_id)
        await msg.answer(text=text.get("analis_not_found"))
    else:
        analis_values: List[ReturnAnalisValue] = get_analis_values_by_analis_id(
            id=int(msg.text)
        )
        if analis_values is not None:
            message = ""
            for value in analis_values:
                message += text.get("get_analis_value_elem").format(
                    id=value.id, value=value.value, date=value.date
                )
            await state.set_data({"analis_id": int(msg.text)})
            await msg.answer(
                text="Введи ID того анализа, значения которого что ты хочешь удалить:\n\n"
                + message,
                reply_markup=commands_keyboard(),
            )
            await state.set_state(DeleteAnalisId.analis_value_id)
        else:
            await msg.answer(
                text=text.get("analises_not_found"), reply_markup=commands_keyboard()
            )
            await state.clear()


@router.message(F.text, DeleteAnalisId.analis_value_id)
async def delete_analis_value_by_id_handler(msg: Message, state: FSMContext):
    if not msg.text.isdigit:
        await state.set_state(DeleteAnalisId.analis_id)
        await msg.answer(text=text.get("get_analis_id_fail"))
    else:
        analis_id = await state.get_data()
        deleting = delete_analis_value(
            value_id=int(msg.text), analis_id=analis_id.get("analis_id")
        )

        if deleting == 204:
            await msg.answer(
                text=text.get("deleting_analis_value"), reply_markup=commands_keyboard()
            )
            await state.clear()
        else:
            await msg.answer(
                text=text.get("deleting_not_found"), reply_markup=commands_keyboard()
            )
            await state.clear()
