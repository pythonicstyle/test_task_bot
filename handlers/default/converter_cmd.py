from datetime import datetime
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text

from keyboards.cancel_button import cancel_kb
from loader import dp, bot
from config.config import CONVERTER_API_KEY
from keyboards.reply_keyboard import main_menu_kb


class ConverterStates(StatesGroup):
    from_cur = State()
    to_cur = State()
    amount = State()


@dp.message_handler(Text(equals="cancel"), state='*')
async def return_menu(message: types.Message, state: FSMContext) -> None:
    if state is None:
        return
    await state.finish()
    await message.answer(text="Вы вернулись в главное меню",
                         reply_markup=main_menu_kb())


@dp.message_handler(Text(equals="converter currency"))
async def converter_start(message: types.Message) -> None:
    await bot.send_message(message.chat.id,
                           text="Введите валюту, которую будем конвертировать",
                           reply_markup=cancel_kb())
    await ConverterStates.from_cur.set()
    await message.delete()


@dp.message_handler(state=ConverterStates.from_cur)
async def handle_first_currency(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if len(message.text) == 3 and message.text.isalpha():
            data['from_cur'] = message.text
            await message.reply(text="Теперь введите валюту, в которую нужно сконвертировать",
                                reply_markup=cancel_kb())
            await ConverterStates.next()
        else:
            await message.answer("Введите 3-буквенное значение аббревиатуры на английском языке")
            await ConverterStates.from_cur.set()


@dp.message_handler(state=ConverterStates.to_cur)
async def handle_second_currency(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if len(message.text) == 3 and message.text.isalpha():
            data['to_cur'] = message.text
            await message.reply(text="Осталось ввести сумму",
                                reply_markup=cancel_kb())
            await ConverterStates.next()
        else:
            await message.answer("Введите 3-буквенное значение аббревиатуры на английском языке")
            await ConverterStates.to_cur.set()


@dp.message_handler(state=ConverterStates.amount)
async def handle_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.isdigit():
            data['amount'] = int(message.text)
            await message.reply("Выполняю конвертацию...")
            await state.finish()

            try:
                from_cur = data["from_cur"]
                to_cur = data["to_cur"]
                amount = data["amount"]

                url = f"https://api.apilayer.com/exchangerates_data/convert?" \
                      f"to={to_cur}&from={from_cur}&amount={amount}"
                payload = {}
                headers = {
                    "apikey": CONVERTER_API_KEY
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                data = response.json()

                today = datetime.fromtimestamp(data["info"]["timestamp"])
                summ = data["query"]["amount"]
                init_currency = data["query"]["from"]
                result = round(data["result"], 3)
                currency = data["query"]["to"]

                await message.answer(f"{today}\n"
                                     f"<b>{summ} {init_currency} is {result} {currency}</b>",
                                     reply_markup=main_menu_kb())
                await message.delete()

            except Exception:
                await message.answer("К сожалению, я не смог обработать такой запрос 😢"
                                     "попробуйте ввести корректные данные ещё раз",
                                     reply_markup=main_menu_kb())
        else:
            await message.answer("Введите корректную сумму")
            await ConverterStates.amount.set()
