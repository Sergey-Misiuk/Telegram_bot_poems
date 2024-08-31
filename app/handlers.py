from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import app.database.requests as rq
import app.keyboards as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)  # type: ignore
    await message.answer("Hi!\nI'm a poetry telegram bot", reply_markup=kb.main)


@router.message(F.text == "Случайный стих")
async def random_poetry(message: Message):
    set_poetry = await rq.get_random_poetry()
    await message.answer(
        f"Стих\n\n{set_poetry['author']}\n\n{set_poetry['poem_name']}\n\n{set_poetry['poem_text']}",
        reply_markup=await kb.poetry(),
    )


@router.message(F.text == "Авторский стих")
async def get_personal_poetry(message: Message):
    pass


@router.callback_query(F.data.startswith("to_favourite"))
async def category(callback: CallbackQuery):
    print(callback.message.text.split('\n'))   # type: ignore
    await callback.answer("Стих добавлен в избранные!")
