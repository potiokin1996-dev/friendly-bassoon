from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import OpenAI
import asyncio
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

client = OpenAI(api_key=OPENAI_API_KEY)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Напиши тему поста.")

@dp.message()
async def generate_post(message: types.Message):

    prompt = f"""
    Напиши Telegram-пост для канала про AI и бизнес.

    Тема: {message.text}

    Стиль:
    - коротко
    - уверенно
    - практично
    - без воды
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    post = response.choices[0].message.content

    await message.answer(post)

    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=post
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
