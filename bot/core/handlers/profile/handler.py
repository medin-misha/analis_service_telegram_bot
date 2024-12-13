from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram import Router, F

from .messages import text, genders
from .states import GetUserData
from .keyboards import gender_keyboard, commands_keyboard
from .utils import create_user, get_user_by_name
from .validators import CreateUser, ReturnUser

router = Router()


@router.message(Command("profile"))
async def create_user_profile(msg: Message, state: FSMContext):
    try:
        user_profile_data: ReturnUser = get_user_by_name(user_name=msg.from_user.username)
        await msg.answer(
            text=text.get("profile_info").format(
                name=user_profile_data.name,
                age=user_profile_data.age,
                weight=user_profile_data.weight,
                gender="мальчик" if user_profile_data.gender else "девочка",
            ),
            reply_markup=commands_keyboard(),
        )
        await state.clear()
    except:
        await msg.answer(text=text.get("create_profile"))
        await state.set_state(GetUserData.age)


@router.message(F.text, GetUserData.age)
async def set_age(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer(text=text.get("fail_int").format("возраст"))
        await state.set_state(GetUserData.age)
    else:
        await state.set_data({"name": msg.from_user.username, "age": int(msg.text)})
        await msg.answer(text=text.get("age_success"))
        await state.set_state(GetUserData.weight)


@router.message(F.text, GetUserData.weight)
async def set_weight(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer(text=text.get("fail_int").format("вес"))
        await state.set_state(GetUserData.age)
    else:
        user_data: dict = await state.get_data()
        user_data["weight"] = int(msg.text)
        await state.set_data(user_data)
        await msg.answer(
            text=text.get("weight_success"), reply_markup=gender_keyboard()
        )
        await state.set_state(GetUserData.gender)


@router.message(F.text, GetUserData.gender)
async def get_gender(msg: Message, state: FSMContext):
    if not msg.text in genders:
        await state.set_state(GetUserData.gender)
        await msg.answer(text=text.get("fail_gender"))
    else:
        user_data: dict = await state.get_data()
        user_data["gender"] = True if msg.text == genders[0] else False
        await state.set_data(user_data)

        user_data: ReturnUser = create_user(user_data=user_data)

        await msg.answer(
            text=text.get("profile_info").format(
                name=user_data.name,
                age=user_data.age,
                weight=user_data.weight,
                gender="мальчик" if user_data.gender else "девочка",
            ), reply_markup=commands_keyboard()
        )
        await state.clear()
