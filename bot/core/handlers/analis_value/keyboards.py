from aiogram.utils.keyboard import ReplyKeyboardBuilder
from .messages import now_date


def analis_value_date():
    builder = ReplyKeyboardBuilder()

    builder.button(text=now_date)
    return builder.as_markup()


def analis_keyboard_builder(analises: list):
    builder = ReplyKeyboardBuilder()

    for analis in analises:
        builder.button(text=f"{analis.get("id")}")
    return builder.as_markup()


def analises_not_found():
    builder = ReplyKeyboardBuilder()

    builder.button(text="/create_analis")
    return builder.as_markup()


def commands_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(text="/profile")

    builder.button(text="/create_analis")
    builder.button(text="/get_analis")
    builder.button(text="/delete_analis")

    builder.button(text="/analis_values")
    builder.button(text="/create_value")
    builder.button(text="/delete_analis_value")

    return builder.as_markup()
