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


@app.get("/{path_param}")
async def with_params(path_param: int, query_param: str):
    return {
        "path": path_param,
        "query_param": query_param,
    }
