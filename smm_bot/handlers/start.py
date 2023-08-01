from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from templates import render_template
from services.add_user import insert_user

async def start(message: Message):
    await insert_user(message.from_user.id)
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Перейти к следующему видео", callback_data="goto_video2")
    keyboard.add(button)
    await message.answer(render_template("start.j2"), reply_markup=keyboard)