from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def hello():
    return {"Hello": "World"}


@app.get("/{path_param}")
def with_params(path_param: int, query_param: str):
    return {
        "path": path_param,
        "query_param": query_param,
    }


# # TODO after https://github.com/encode/uvicorn/issues/492 is solved use the factory app
# async def asgi_app(scope, receive, send):
#     app = FastAPI()
#     app.add_route('/', hello, methods=['get'])
#     app.add_api_route('/', hello, methods=['get'])
#     await app(scope, receive, send)


# TODO setup pylint, mypy
