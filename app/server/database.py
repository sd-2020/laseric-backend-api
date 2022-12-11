import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config

MONGO_DETAILS = config("MONGO_DETAILS")  # read environment variable

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.users

users_collection = database.get_collection("users_collection")

version_collection = database.get_collection("version_collection")

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "fullname": user["fullname"],
        "machinekey": user["machinekey"],
        "secretkey": user["secretkey"],
        "isAuthorized": user["isAuthorized"],
        "isSecretUsed": user["isSecretUsed"],
    }

def version_helper(body) -> dict:
    return {
        "id": str(body["_id"]),
        "version": body["version"],
        "url": body["url"]
    }


async def get_version() -> dict:
    # response = await version_collection.find()
    # print(response)
    versions = []
    async for v in version_collection.find():
        versions.append(version_helper(v))
    return versions[0]

async def update_version(id: str, data: dict):
    if len(data) < 1:
        return False
    version = await version_collection.find_one({"_id": ObjectId(id)})
    if version:
        updated_version = await version_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_version:
            return True
        return False

async def add_version(user_data: dict) -> dict:
    user = await version_collection.insert_one(user_data)
    new_user = await version_collection.find_one({"_id": user.inserted_id})
    return version_helper(new_user)

async def retrieve_users():
    users = []
    async for student in users_collection.find():
        users.append(user_helper(student))
    return users

async def add_user(user_data: dict) -> dict:
    user = await users_collection.insert_one(user_data)
    new_user = await users_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


async def retrieve_user(id: str) -> dict:
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)

async def retrieve_user_by_secret(secretkey: str) -> dict:
    user = await users_collection.find_one({"secretkey": secretkey})
    if user:
        return user_helper(user)

async def retrieve_user_by_machine(machinekey: str) -> dict:
    user = await users_collection.find_one({"machinekey": ObjectId(machinekey)})
    if user:
        return user_helper(user)

async def update_user(id: str, data: dict):
    if len(data) < 1:
        return False
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await users_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False

async def delete_user(id: str):
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if user:
        await users_collection.delete_one({"_id": ObjectId(id)})
        return True
