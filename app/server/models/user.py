from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    fullname: str = Field(...)
    machinekey: str = Field(...)
    secretkey: str = Field(...)
    version: str = Field(...)
    isAuthorized: bool = Field(...)
    isSecretUsed: bool = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "machinekey": "XXXXXXXXXXXXXX",
                "secretkey": "XXXXXXXXXXXXXX",
                "isAuthorized": False,
                "isSecretUsed": False,
                "version": ""
            }
        }

class UpdateUserModel(BaseModel):
    fullname: Optional[str]
    machinekey: Optional[str]
    secretkey: Optional[str]
    version: Optional[str]
    isAuthorized: Optional[str]
    isSecretUsed: Optional[str]

    class Config:
        schema_extra = {
             "example": {
                "fullname": "John Doe",
                "machinekey": "XXXXXXXXXXXXXX",
                "secretkey": "XXXXXXXXXXXXXX",
                "isAuthorized": False,
                "isSecretUsed": False,
                "version": ""
            }
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
