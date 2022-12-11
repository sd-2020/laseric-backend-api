from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class VersionSchema(BaseModel):
    version: str = Field(...)
    url: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "version": "1.0.0",
                "url": "http://google.com"
            }
        }

class UpdateVersionModel(BaseModel):
    version: Optional[str]
    url:  Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "version": "1.0.0",
                "url": "http://google.com"
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
