"""
Internal services of the application. The IoC container of the application.
"""

from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .db_models import get_db_session_factory

db_session_creator: ContextVar[async_sessionmaker[AsyncSession]] = ContextVar("db_session_creator")


def init():
    db_session_creator.set(get_db_session_factory())
