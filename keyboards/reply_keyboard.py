from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu_kb() -> ReplyKeyboardMarkup:
    main_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="check current weather"),
                KeyboardButton(text="converter currency")
            ],
            [
                KeyboardButton(text="add cuteness"),
                KeyboardButton(text="get pool")
            ],
        ], resize_keyboard=True, one_time_keyboard=True
    )

    return main_menu
