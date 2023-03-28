import datetime

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import expression

from sample_backend.config import Config


def make_db_session_creator() -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(Config().postgres_url)
    # Don't expire objects when a commit is made.
    # Expired objects need to be refreshed from the DB.
    # With this we can get the IDs of freshly inserted objects without additional DB interactions,
    # because SQLAlchemy does inserts with "INSERT...RETURNING" query.
    return async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Note(Base):
    __tablename__ = "notes"

    # TODO make this a GUID
    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO should be timezone-aware
    creation_date: Mapped[datetime.datetime] = mapped_column(server_default=func.now())  # pylint: disable=not-callable
    contents: Mapped[str]
    is_deleted: Mapped[bool] = mapped_column(server_default=expression.false())
