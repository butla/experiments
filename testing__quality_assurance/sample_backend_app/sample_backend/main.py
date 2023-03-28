import fastapi

from . import services

# TODO notes API with CRD, where D only marks stuff as deleted

app = fastapi.FastAPI()


@app.on_event("startup")
async def startup():
    services.init()


@app.get("/")
async def hello():
    return {"Hello": "World"}


@app.get("/notes")
async def get_all_notes():
    return {"Hello": "World"}


@app.get("/notes/{note_id}")
async def get_all_notes(node_id: int):
    return {"Hello": "World"}


@app.post("/{path_param}")
async def new_note(path_param: int, query_param: str):
    return {
        "path": path_param,
        "query_param": query_param,
    }
