import fastapi

from . import api_schemas, services

app = fastapi.FastAPI()


@app.on_event("startup")
async def startup():
    services.init()


@app.get("/")
async def hello():
    return {"hello": "world"}


@app.get("/notes/", response_model=list[api_schemas.NoteResponsePayload])
async def get_all_notes():
    return await services.get_notes_repo().get_all()


@app.get("/notes/{note_id}/", response_model=api_schemas.NoteResponsePayload)
async def get_note_by_id(note_id: int):
    note = await services.get_notes_repo().get(note_id)
    return note


@app.post("/notes/", response_model=api_schemas.NoteResponsePayload, status_code=201)
async def new_note(note_payload: api_schemas.NoteCreationPayload):
    notes_repo = services.get_notes_repo()
    note_id = await notes_repo.create(note_payload)
    return await notes_repo.get(note_id)


# TODO add the delete endpoint
