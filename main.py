import asyncio
import requests
import os
from gtts import gTTS
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram import Bot, Dispatcher, F
from googletrans import Translator

from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()  # Инициализация переводчика


@dp.message(F.photo)
async def react_photo(message: Message):
	await bot.download(message.photo[-1],destination=f'img/{message.photo[-1].file_id}.jpg')

@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("sample.ogg")
    await message.answer_voice(voice)

@dp.message(F.text == "Какая погода в Москве?")
async def aitext(message: Message):
    response = requests.get("https://wttr.in/Moscow?format=3")
    weather = response.text.strip()
    await message.answer(weather)

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я скажу тебе про погоду в Москве")

@dp.message()
async def translate_message(message: Message):  # Изменил название функции
    translation = translator.translate(message.text, dest='en')
    await message.answer(f"🇬🇧 Перевод: {translation.text}")

    tts = gTTS(text=translation.text, lang='en')
    tts.save("translation.ogg")
    audio = FSInputFile('translation.ogg')
    await bot.send_audio(message.chat.id, audio)
    os.remove("translation.ogg")




async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())