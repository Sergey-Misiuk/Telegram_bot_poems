from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import app.database.requests as rq
import app.keyboards as kb
import app.state as st

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)  # type: ignore
    if message.from_user.id == 1868378315:   # type: ignore
        await message.answer(
            "Hi!\nI'm a poetry telegram bot", reply_markup=kb.admin_main
        )
    else:
        await message.answer("Hi!\nI'm a poetry telegram bot", reply_markup=kb.main)


@router.message(F.text == "Случайный стих")
async def random_poetry(message: Message):
    set_poetry = await rq.get_random_poetry()
    await message.answer(
        f"Стих\n\n{set_poetry.author}\n\n{set_poetry.title}\n\n{set_poetry.text}",
        reply_markup=await kb.poetry(),
    )


@router.message(F.text == "Список авторских стихов")
async def get_personal_poetry(message: Message):

    keyboard = await kb.personal_poems()  # type: ignore[union-attr]

    if keyboard.inline_keyboard:
        await message.answer(
            "Список авторский стихов!",
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            "Пока здесь нет авторских стихов\nНо скоро они обязательно появяться.",
            reply_markup=keyboard,
        )


@router.message(F.text == "Список избранных стихов")
async def get_all_poetry(message: Message):
    await rq.set_user(message.from_user.id)  # type: ignore[union-attr]
    keyboard = await kb.poems(message.from_user.id)  # type: ignore[union-attr]
    if keyboard.inline_keyboard:
        await message.answer(
            "Список ваших избранных стихов!",
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            "Пока здесь нет ваших любимых стихов\nДобавьте понравившийся стих в избранные.",
            reply_markup=keyboard,
        )


@router.callback_query(F.data == "to_favourite")
async def add_poetry(callback: CallbackQuery):
    await rq.add_or_del_fvourite_poetry(
        callback.message.chat.id, callback.message.text.split("\n")  # type: ignore[union-attr]
    )
    await callback.answer("Стих добавлен в избранные!")
    await callback.message.edit_reply_markup(reply_markup=await kb.del_poetry())  # type: ignore[union-attr]


@router.callback_query(F.data == "del_favourite")
async def del_poetry(callback: CallbackQuery):
    await rq.add_or_del_fvourite_poetry(
        callback.message.chat.id, callback.message.text.split("\n")  # type: ignore[union-attr]
    )
    await callback.answer("Стих удален из избранных!")
    await callback.message.edit_reply_markup(reply_markup=await kb.poetry())  # type: ignore[union-attr]


@router.callback_query(F.data.startswith("poem_"))
async def poem_info(callback: CallbackQuery):
    item_date = await rq.get_poem(callback.data.split("_")[1])  # type: ignore[union-attr]
    await callback.answer("")

    exist_poem = await rq.exist_poem_db(item_date.id, callback.message.chat.id)  # type: ignore[union-attr]
    if exist_poem:
        await callback.message.answer(  # type: ignore[union-attr]
            f"Стих\n\n{item_date.author}\n\n{item_date.title}\n\n{item_date.text}",
            reply_markup=await kb.del_poetry(),
        )
    else:
        await callback.message.answer(  # type: ignore[union-attr]
            f"Стих\n\n{item_date.author}\n\n{item_date.title}\n\n{item_date.text}",
            reply_markup=await kb.poetry(),
        )


@router.message(F.text == "Админ панель")
async def admin(message: Message):
    keyboard = kb.admin_panel

    await message.answer("Добро пожаловать в админ меню", reply_markup=keyboard)


@router.message(F.text == "На главную")
async def to_main_page(message: Message):
    keyboard = kb.admin_main

    await message.answer("Переход в главное меню", reply_markup=keyboard)


@router.message(F.text == "Добавить стих")
async def add_poem(message: Message, state: FSMContext):

    await state.set_state(st.Reg_poem.title)
    await message.answer("Введите название вашего стиха")


@router.message(st.Reg_poem.title)
async def add_poem_first(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(st.Reg_poem.text)
    await message.answer("Введите текст стиха")


@router.message(st.Reg_poem.text)
async def add_poem_second(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await rq.set_poem(data)
    await message.answer("Стих добавлен")
