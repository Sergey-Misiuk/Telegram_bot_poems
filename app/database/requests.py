import logging
from typing import Any
from app.database.models import async_session, Favourite, Poem, User
from sqlalchemy import select, delete

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
        poem = await session.scalar(
            select(Poem).where(
                Poem.author == random_poetry.author, Poem.title == random_poetry.title
            )
        )

        if not poem:
            logging.info("Стих отсутствует в базе данных, добавляю в базу")
            session.add(
                Poem(
                    author=random_poetry.author,
                    title=random_poetry.title,
                    text=random_poetry.text,
                )
            )
            await session.commit()
            return random_poetry
        logging.info("Стих взят из базы данных")
        return poem


async def add_or_del_fvourite_poetry(tg_id, poetry):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        poem = await session.scalar(
            select(Poem).where(Poem.title == poetry[4]).where(Poem.author == poetry[2])
        )
        # print()
        # print(poetry)
        # print()
        # print(poem)
        # print()
        # print()
        favorite_poem = await session.scalar(
            select(Favourite)
            .where(Favourite.poem_id == poem.id)
            .where(Favourite.user_id == user.id)
        )
        if not favorite_poem:
            session.add(Favourite(poem_id=poem.id, user_id=user.id))
            await session.commit()
        else:
            await session.execute(
                delete(Favourite).where(
                    Favourite.poem_id == poem.id, Favourite.user_id == user.id
                )
            )
            await session.commit()


async def get_favourite_poetry(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        poems = await session.scalars(
            select(Favourite).where(Favourite.user_id == user.id)
        )

        return poems


async def get_personal_poetry():
    async with async_session() as session:
        poems = await session.scalars(select(Poem).where(Poem.author == "Авторский"))

        return poems


async def get_poem(poem_id):
    async with async_session() as session:
        return await session.scalar(select(Poem).where(Poem.id == poem_id))


async def exist_poem_db(poem_id, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        poems = await session.scalar(
            select(Favourite)
            .where(Favourite.user_id == user.id)
            .where(Favourite.poem_id == poem_id)
        )
        return poems
