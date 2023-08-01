from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from templates import render_template

async def video2(call: CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Перейти к третьему видео", callback_data="goto_video3")
    keyboard.add(button)
    await call.message.edit_text(render_template("video2.j2"), reply_markup=keyboard)
