from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    update_version,
    get_version,
    add_version
)

from app.server.models.version import (
    ErrorResponseModel,
    ResponseModel,
    VersionSchema,
    UpdateVersionModel
)

router = APIRouter()

@router.post("/", response_description="user data added into the database")
async def add_user_data(user: VersionSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_version(user)
    return ResponseModel(new_user, "version added successfully.")


@router.get("/", response_description="version retrieved")
async def get_users():
    version = await get_version()
    if version:
        return ResponseModel(version, "Latest")
    return ResponseModel({}, "Not Found")


@router.put("/{id}")
async def update_user_data(id: str, req: UpdateVersionModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_version = await update_version(id, req)
    if updated_version:
        return ResponseModel(
            "Version with ID: {} is updated successful".format(id),
            "Updated",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the data.",
    )