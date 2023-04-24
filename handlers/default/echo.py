from loader import dp, bot
from aiogram import types


@dp.message_handler(content_types=['photo', 'video', 'emoji'])
async def foo(message: types.Message) -> None:
    await bot.send_message(chat_id=message.chat.id,
                           text="Здорово!")