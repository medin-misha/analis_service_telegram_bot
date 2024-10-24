from aiogram.utils.keyboard import ReplyKeyboardBuilder
from .messages import genders


def gender_keyboard():
    builder = ReplyKeyboardBuilder()

    for gender in genders:
        builder.button(text=gender)
    return builder.as_markup()

def profile_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(text="кнопка")
    builder.button(text="кнопка")
    builder.button(text="кнопка")
    builder.button(text="кнопка")
    return builder.as_markup()