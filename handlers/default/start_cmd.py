from datetime import datetime
from aiogram import types
from aiogram.dispatcher.filters import Text
import logging

from keyboards.reply_keyboard import main_menu_kb
from loader import bot, dp

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message) -> None:

    user_id = message.from_user.id
    user_fullname = message.from_user.full_name
    greeting = f"<b>Здравствуйте, {message.from_user.first_name}!</b>"
    await bot.send_message(message.from_user.id,
                           text=f"{greeting}\nВыберите дальнейшее действие из меню",
                           reply_markup=main_menu_kb())
    logging.info(f"{user_id=} {user_fullname=} - {datetime.now()}")


@dp.message_handler(Text(equals="Привет"))
async def say_hello(message: types.Message):
    await message.reply(text=f"И тебе привет, {message.from_user.first_name}!")