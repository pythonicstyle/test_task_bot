import requests
from aiogram import types
from datetime import datetime
from aiogram.dispatcher.filters import Text

from loader import dp
from config.config import WEATHER_API_KEY


@dp.message_handler(Text(equals="check current weather"))
async def check_weather_command(message: types.Message) -> None:
    await message.answer(text="Отлично!\nЧтобы узнать погоду, ведите название города")


@dp.message_handler(content_types=["text"])
async def actual_weather(message: types.Message) -> None:
    if message.text.isalpha():
        response = requests.get(url=f'https://api.openweathermap.org/data/2.5/weather?q={message.text.lower()}'
                                    f'&appid={WEATHER_API_KEY}&units=metric', )
        try:
            data = response.json()

            city = data["name"]
            country = data["sys"]["country"]

            temperature = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            precipitations = data["weather"][0]["description"]
            pressure = data["main"]["pressure"]
            visibility = data["visibility"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            wind_direction = data["wind"]["deg"]
            sunrise_timestamp = datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.fromtimestamp(data["sys"]["sunset"])

            await message.reply(
                f"Погода в городе: <b>{city}, {country}</b>\n"
                f"Температура: {temperature} C° | Ощущается как: {feels_like} C°\n"
                f"Ветер: {wind_direction}° | {wind_speed} м/с\n"
                f"Осадки: {precipitations} | Видимость: {visibility} м\n"
                f"Влажность воздуха: {humidity} % | Давление: {pressure} мм.рт.ст\n"
                f"Восход солнца: {sunrise_timestamp}\n"
                f"Закат солнца: {sunset_timestamp}\n"
            )

        except Exception:
            await message.answer("К сожалению, я не смог найти информацию о погоде по вашему запросу 😢")
    else:
        await message.answer(f"По запросу '{message.text}' ничего не найдено")
