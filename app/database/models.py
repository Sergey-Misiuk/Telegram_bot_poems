import os
from typing import List
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)

DB_URL: str = os.environ.get("DATABASE_URL")  # type: ignore

engine = create_async_engine(url=DB_URL, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class Poem(Base):
    __tablename__ = "poems"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    text: Mapped[str] = mapped_column(String(1000))
    author: Mapped[int] = mapped_column(String(500))

    def __repr__(self) -> str:
        return f"Poem(title={self.title}, author={self.author}, text={self.text})"


class Favourite(Base):
    __tablename__ = "favourites"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    poem_id: Mapped[int] = mapped_column(ForeignKey("poems.id"))

    poem_info: Mapped[List[Poem]] = relationship(
        "Poem",
        lazy="subquery",
    )


async def create_database():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)
