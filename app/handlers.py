from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

import app.database.requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)   # type: ignore
    await message.answer("Hi!\nI'm a telegram bot")
