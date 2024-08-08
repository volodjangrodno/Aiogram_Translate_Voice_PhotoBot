import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import FSInputFile, Message
import asyncio
from deep_translator import GoogleTranslator
from config import TOKEN
from gtts import gTTS


# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Инициализация переводчика
translator = GoogleTranslator(source='auto', target='en')

# Создание папки для хранения изображений, если её нет
if not os.path.exists('img'):
    os.makedirs('img')

@dp.message(F.photo)
async def photos(message: Message):
    photo = message.photo[-1]
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name = f'img/{file_id}.jpg'

    await bot.download_file(file_path, file_name)
    await message.reply("Фото сохранено!")

@dp.message(Command('voice'))
async def send_voice_message(message: Message):
    voice_file = FSInputFile('voices/audio.ogg')
    await bot.send_voice(chat_id=message.chat.id, voice=voice_file)

@dp.message(F.text)
async def translate_text(message: Message):
    translated_text = translator.translate(message.text)
    await message.reply(f"Перевод: {translated_text}")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Я бот для перевода текста и голосового сообщения.")

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n /start \n /help \n /voice")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())