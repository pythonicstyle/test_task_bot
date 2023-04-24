from aiogram import types
from aiogram.dispatcher.filters import Text
import random
import os

from loader import dp, bot
from keyboards.reply_keyboard import main_menu_kb


DIRECTORY = '/Users/antongaranin/PycharmProjects/pythonProject/test_case_bot/uploads/images'


@dp.message_handler(Text(equals="add cuteness"))
async def check_weather_command(message: types.Message) -> None:
    files = os.listdir(DIRECTORY)
    file = random.choice(files)
    photo = open(os.path.join(DIRECTORY, file), 'rb')
    await bot.send_photo(chat_id=message.chat.id,
                         photo=photo,
                         caption="Держи!",
                         reply_markup=main_menu_kb())




