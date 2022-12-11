from fastapi import FastAPI

from app.server.routes.user import router as UserRouter
from app.server.routes.version import router as VersionRouter

app = FastAPI()

app.include_router(VersionRouter, tags=["Version"], prefix="/version")
app.include_router(UserRouter, tags=["Client"], prefix="/client")


# @app.get("/", tags=["Root"])
# async def read_root():
#     return {"message": "Welcome to this fantastic app!"}
