from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="cancel")
            ]
        ], resize_keyboard=True
    )

    return kb
