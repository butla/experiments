import fastapi

# TODO SQL DB - don't run anything on import
# TODO notes API with CRD, where D only marks stuff as deleted
# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm
# psycopg3 usage: db_string = "postgresql+psycopg://user:password@db/psycoptest"

app = fastapi.FastAPI()


@app.get("/")
async def hello():
    return {"Hello": "World"}


@app.get("/{path_param}")
async def with_params(path_param: int, query_param: str):
    return {
        "path": path_param,
        "query_param": query_param,
    }
