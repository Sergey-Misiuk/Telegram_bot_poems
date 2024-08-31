from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

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
