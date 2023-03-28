"""
Internal services of the application.
The IoC container of the application.
"""

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .db import make_db_session_creator
from .notes import NotesRepository

_db_session_creator: Optional[async_sessionmaker[AsyncSession]]
_notes_repo: Optional[NotesRepository]


def get_db_session_creator() -> async_sessionmaker[AsyncSession]:
    if _db_session_creator is None:
        raise LookupError("Init wasn't run!")
    return _db_session_creator


def get_notes_repo() -> NotesRepository:
    if _notes_repo is None:
        raise LookupError("Init wasn't run!")
    return _notes_repo


def init():
    global _db_session_creator  # pylint: disable=global-statement
    global _notes_repo  # pylint: disable=global-statement
    _db_session_creator = make_db_session_creator()
    _notes_repo = NotesRepository(_db_session_creator)
