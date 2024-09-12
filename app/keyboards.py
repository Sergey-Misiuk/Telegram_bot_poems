from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_favourite_poetry

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Случайный стих")],
        [KeyboardButton(text="Авторский стих")],
        [KeyboardButton(text="Список избранных стихов")],
        [KeyboardButton(text="Оставить отзыв"), KeyboardButton(text="О нас")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбирите пункт из меню...",
)


async def poetry():
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Добавить в избранные", callback_data="to_favourite")
    )
    return keyboard.adjust(1).as_markup()


async def del_poetry():
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(
            text="Удалить из избранного", callback_data="del_favourite"
        )
    )
    return keyboard.adjust(1).as_markup()


async def poems(tg_id):
    poems = await get_favourite_poetry(tg_id)
    keyboard = InlineKeyboardBuilder()

    for poem in poems:
        keyboard.add(
            InlineKeyboardButton(
                text=f'"{poem.poem_info.title}" - {poem.poem_info.author}',
                callback_data=f"poem_{poem.poem_id}",
            )
        )
    return keyboard.adjust(1).as_markup()
