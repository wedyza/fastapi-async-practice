
from fastapi import FastAPI

from src.app.endpoints import create_api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="test web",
        version="0.1.0",
    )
    app.include_router(create_api_router())
    return app


app = create_app()

# async def run_web_app() -> None:
#     server = uvicorn.Server(
#         uvicorn.Config(
#             app=app,
#             host="localhost",
#             port=8000
#         )
#     )
#     await server.serve()

# async def async_main() -> None:
#     async with asyncio.TaskGroup() as task_group:
#         task_group.create_task(run_web_app())

# if __name__ == '__main__':
#     asyncio.run(async_main())
