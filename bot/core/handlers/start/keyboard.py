from aiogram.utils.keyboard import ReplyKeyboardBuilder
from .messages import texts


def start_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text=texts.get("profile_button"))
    return builder.as_markup()
