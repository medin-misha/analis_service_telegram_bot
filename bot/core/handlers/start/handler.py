from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from .messages import texts
from .keyboard import start_keyboard

router = Router()


@router.message(Command("start"))
async def start(msg: Message):
    await msg.answer(
        text=texts.get("start").format(msg.from_user.username),
        reply_markup=start_keyboard(),
    )
