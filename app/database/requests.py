import logging
from typing import Any
from app.database.models import async_session, Favourite, Poem, User
from sqlalchemy import select

from app.functions import parser_poetry


async def set_user(tg_id: Any):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_random_poetry():
    random_poetry = await parser_poetry()
    async with async_session() as session:
        poem = await session.scalar(select(Poem).where(Poem.author == random_poetry.author, Poem.title == random_poetry.title))

        if not poem:
            logging.info('Стих отсутствует в базе данных, добавляю в базу')
            session.add(Poem(author=random_poetry.author, title=random_poetry.title, text=random_poetry.text))
            await session.commit()
            return random_poetry
        logging.info('Стих взят из базы данных')
        return poem


async def set_poetry(tg_id, poetry):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        poem = await session.scalar(select(Poem).where(Poem.title == poetry))
        session.add(Favourite(poem=poem.id, user=user.id))
        await session.commit()
