from bson import ObjectId

from schemas import TodoResponseSchema
from models import TodoModel, UserModel
from database import get_todo_collection, get_user_collection

todo_collection = get_todo_collection()
user_collection = get_user_collection()

async def create_todo(todo: TodoModel) -> TodoModel:
    todo_dict = todo.dict()
    result = await todo_collection.insert_one(todo_dict)
    todo_dict["id"] = str(result.inserted_id)
    return TodoResponseSchema(**todo_dict)

async def get_todo_by_id(id: str) -> TodoResponseSchema:
    todo = await todo_collection.find_one({"_id": ObjectId(id)})
    if todo:
        todo["id"] = str(todo["_id"])
        return TodoResponseSchema(**todo)
    return None

async def get_all_todos():
    todos = []
    async for todo in todo_collection.find():
        todo["id"] = str(todo["_id"])
        todos.append(TodoResponseSchema(**todo))
    return todos

async def update_todo(id: str, todo_data: dict) -> TodoModel:
    await todo_collection.update_one({"_id": ObjectId(id)}, {"$set": todo_data})
    todo = await get_todo_by_id(id)
    return todo

async def delete_todo(id: str):
    await todo_collection.delete_one({"_id": ObjectId(id)})

# New functions for user operations
async def create_user(user: UserModel) -> UserModel:
    result = await user_collection.insert_one(user.dict())
    user.id = result.inserted_id
    return user

async def get_user_by_username(username: str) -> UserModel:
    user = await user_collection.find_one({"username": username})
    if user:
        return UserModel(**user)
    else:
        return None
