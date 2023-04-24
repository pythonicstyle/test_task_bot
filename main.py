from aiogram.utils import executor

from loader import dp

from handlers import default


async def on_startup(_) -> None:
    print("Bot has been started up")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
