import pytest
from sqlalchemy import select

from sample_backend import api_schemas
from sample_backend.db import Note, make_db_session_creator
from sample_backend.notes import NotesRepository


@pytest.fixture
def notes_repo():
    return NotesRepository(make_db_session_creator())


@pytest.mark.asyncio
async def test_create_a_note(notes_repo: NotesRepository):
    note_payload = api_schemas.NoteCreationPayload(contents="I'm a note, wee!")

    id_ = await notes_repo.create(note_payload)

    async with make_db_session_creator()() as session:
        query = select(Note).where(Note.id == id_)
        result = await session.execute(query)
        saved_object = result.scalar()

    assert saved_object.contents == note_payload.contents
    assert saved_object.id == id_


# TODO cover the rest of NotesRepository methods

# TODO gotta look into __eq__ implementations for SQLAlchemy
# https://stackoverflow.com/questions/39043003/comparing-sqlalchemy-object-instances-for-equality-of-attributes
# https://groups.google.com/g/sqlalchemy/c/fsLODvEAXtY?pli=1
