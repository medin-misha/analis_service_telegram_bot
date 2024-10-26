from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_analis_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(text="/get_analis")
    builder.button(text="/create_analis")
    builder.button(text="/delete_analis")
    builder.button(text="/profile")
    return builder.as_markup()
