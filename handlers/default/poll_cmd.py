from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp, bot
from keyboards.reply_keyboard import main_menu_kb


@dp.message_handler(Text(equals="get pool"))
async def create_poll(message: types.Message):
    await bot.send_poll(chat_id=message.chat.id,
                        question="Какая погода сегодня в вашем городе?",
                        options=[
                            "Отличная ☀️",
                            "Сегодня облачно ⛅️",
                            "Пасмурно ☁️",
                            "Идет дождь 🌩🌨",
                            "Всё еще идет снег ❄️",
                            "Сегодня явно не лучший день для прогулок 🌪",
                            "я живу в Питере",
                        ],
                        allows_multiple_answers=False,
                        is_anonymous=False,
                        reply_markup=main_menu_kb()
                        )
