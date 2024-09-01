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
        f"Стих\n\n{set_poetry.author}\n\n{set_poetry.title}\n\n{set_poetry.text}",
        reply_markup=await kb.poetry(),
    )


@router.message(F.text == "Авторский стих")
async def get_personal_poetry(message: Message):
    pass


@router.callback_query(F.data.startswith("to_favourite"))
async def add_poetry(callback: CallbackQuery):
    s = callback.message.text.split('\n')  # type: ignore
    print(f'{s[2]}    ----   {s[4]}')
    print(callback.message.text)   # type: ignore
    print()   # type: ignore
    # print(callback.message.text.replace('', ' '))   # type: ignore
    # await rq.set_poetry(callback.message.from_user.id, callback.message.text)
    await callback.answer("Стих добавлен в избранные!")
