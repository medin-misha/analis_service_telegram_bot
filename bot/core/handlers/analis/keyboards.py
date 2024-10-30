from aiogram.utils.keyboard import ReplyKeyboardBuilder



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