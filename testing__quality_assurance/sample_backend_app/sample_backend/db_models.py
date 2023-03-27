import datetime

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sample_backend.config import Config


def get_db_session_factory() -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(Config().postgres_url)
    return async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Note(Base):
    __tablename__ = "notes"

    # TODO make this a GUID
    id: Mapped[int] = mapped_column(primary_key=True)
    creation_date: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    contents: Mapped[str]
    is_deleted: Mapped[bool]
