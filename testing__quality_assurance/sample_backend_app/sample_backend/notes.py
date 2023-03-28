"""
Implementation of the repository pattern for notes.

With an app this simple we might not need a repository and just use the ORM directly,
but using the pattern will help illustrate when to use tests at different levels (unit/integrated/functional).

Also, it'll set the stage for using a test double of the NotesRepository in unit tests.
"""

from typing import List

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from . import api_schemas
from .db import Note


class NotesRepository:
    def __init__(self, db_session_creator: async_sessionmaker[AsyncSession]):
        self._db_session_creator = db_session_creator

    async def create(self, note_payload: api_schemas.NoteCreationPayload) -> int:
        """
        Returns:
            The ID under which the note is stored.
        """
        async with self._db_session_creator() as session:
            query = insert(Note).values(contents=note_payload.contents).returning(Note.id)
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    # TODO implement
    async def delete(self):
        pass

    async def get(self, note_id: int) -> Note:
        # TODO handle the case where the ID is not found
        async with self._db_session_creator() as session:
            query = select(Note).where(Note.id == note_id)
            result = await session.execute(query)
            return result.scalar()

    async def get_all(self) -> List[Note]:
        async with self._db_session_creator() as session:
            query = select(Note)
            result = await session.execute(query)
            return result.scalars().all()
