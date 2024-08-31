import os
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)

DB_URL: str = os.environ.get("DATABASE_URL")     # type: ignore

engine = create_async_engine(url=DB_URL, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


# class Author(Base):
#     __tablename__ = "authors"
    
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(50))


class Poem(Base):
    __tablename__ = "poems"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    text: Mapped[str] = mapped_column(String(1000))
    author: Mapped[int] = mapped_column(String(500))
    

class Favourite(Base):
    __tablename__ = 'favourites'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    poem: Mapped[int] = mapped_column(ForeignKey("poems.id"))


async def create_database():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)
