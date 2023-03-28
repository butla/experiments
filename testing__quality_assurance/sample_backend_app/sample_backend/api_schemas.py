import datetime

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class NoteCreationPayload(BaseModel):
    contents: str


class NoteResponsePayload(BaseModel):
    id: int
    creation_date: datetime.datetime
    contents: str

    # With this, FastApi will handle returning ORM Note objects from endpoint functions.
    class Config:
        orm_mode = True
