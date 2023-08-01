from aiogram.types import Message
from templates import render_template

async def other(message: Message):
    await message.answer(render_template("other.j2"))
