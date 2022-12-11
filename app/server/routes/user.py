from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    update_user,
    retrieve_user_by_machine,
    retrieve_user_by_secret
)

from app.server.models.user import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UpdateUserModel,
)

router = APIRouter()

@router.post("/status", response_description="checks status of client")
async def check_data(user: UserSchema = Body(...)):
    fetched_user = await retrieve_user_by_secret(user.secretkey)
    if fetched_user:
        if fetched_user["isSecretUsed"]:
            if user.machinekey == fetched_user["machinekey"]:
                if fetched_user["isAuthorized"] == True:
                    return ResponseModel({ "status": 1 }, "")
                else:
                    return ResponseModel({ "status": 0 }, "")
            else:
                return ResponseModel({ "status": 0 }, "")
        else:
            if fetched_user["machinekey"] == '':
                if fetched_user["isAuthorized"] == True:
                    await update_user(fetched_user['id'], { "machinekey": user.machinekey })
                    await update_user(fetched_user['id'], { "isSecretUsed": True })
                    return ResponseModel({ "status": 1 }, "")
                else:
                    return ResponseModel({ "status": 0 }, "")
            else:
                if user.machinekey == fetched_user["machinekey"]:
                    if fetched_user["isAuthorized"] == True:
                        return ResponseModel({ "status": 1 }, "")
                    else:
                        return ResponseModel({ "status": 0 }, "")
                else:
                    return ResponseModel({ "status": 0 }, "")
    else:
        return ResponseModel({ "status": 0 }, "")

@router.post("/version", response_description="checks status of client")
async def update_version(user: UserSchema = Body(...)):
    fetched_user = await retrieve_user_by_secret(user.secretkey)
    if fetched_user:
        if fetched_user["isSecretUsed"]:
            if user.machinekey == fetched_user["machinekey"]:
                if fetched_user["isAuthorized"] == True:
                    await update_user(fetched_user['id'], { "version": user.version })
                    return ResponseModel({ "status": 1 }, "")
                else:
                    return ResponseModel({ "status": 0 }, "")
            else:
                return ResponseModel({ "status": 0 }, "")
        else:
            if fetched_user["machinekey"] == '':
                await update_user(fetched_user['id'], { "machinekey": user.machinekey })
                await update_user(fetched_user['id'], { "isSecretUsed": True })
                if fetched_user["isAuthorized"] == True:
                    await update_user(fetched_user['id'], { "version": user.version })
                    return ResponseModel({ "status": 1 }, "")
                else:
                    return ResponseModel({ "status": 0 }, "")
            else:
                if user.machinekey == fetched_user["machinekey"]:
                    if fetched_user["isAuthorized"] == True:
                        await update_user(fetched_user['id'], { "version": user.version })
                        return ResponseModel({ "status": 1 }, "")
                    else:
                        return ResponseModel({ "status": 0 }, "")
                else:
                    return ResponseModel({ "status": 0 }, "")
    else:
        return ResponseModel({ "status": 0 }, "")

# @router.post("/", response_description="user data added into the database")
# async def add_user_data(user: UserSchema = Body(...)):
#     user = jsonable_encoder(user)
#     new_user = await add_user(user)
#     return ResponseModel(new_user, "user added successfully.")


# @router.get("/", response_description="users retrieved")
# async def get_users():
#     users = await retrieve_users()
#     if users:
#         return ResponseModel(users, "users data retrieved successfully")
#     return ResponseModel(users, "Empty list returned")


# @router.get("/{id}", response_description="user data retrieved")
# async def get_user_data(id):
#     user = await retrieve_user(id)
#     if user:
#         return ResponseModel(user, "user data retrieved successfully")
#     return ErrorResponseModel("An error occurred.", 404, "user doesn't exist.")


# @router.put("/{id}")
# async def update_user_data(id: str, req: UpdateUserModel = Body(...)):
#     req = {k: v for k, v in req.dict().items() if v is not None}
#     updated_user = await update_user(id, req)
#     if updated_user:
#         return ResponseModel(
#             "user with ID: {} name update is successful".format(id),
#             "user name updated successfully",
#         )
#     return ErrorResponseModel(
#         "An error occurred",
#         404,
#         "There was an error updating the user data.",
#     )


# @router.delete("/{id}", response_description="user data deleted from the database")
# async def delete_user_data(id: str):
#     deleted_user = await delete_user(id)
#     if deleted_user:
#         return ResponseModel(
#             "user with ID: {} removed".format(id), "user deleted successfully"
#         )
#     return ErrorResponseModel(
#         "An error occurred", 404, "user with id {0} doesn't exist".format(id)
#     )
