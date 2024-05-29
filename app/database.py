# from pymongo import MongoClient

# MONGO_URL = "mongodb+srv://21it3031:ivtSUH8HSfjDBMjD@cluster0.4kkffrs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Update this with your MongoDB connection string

# client = MongoClient(MONGO_URL)
# database = client["Todo"]  # Replace "your_database_name" with your database name

# def get_database():
#     return database

# # database = client.todo_database


# todo_collection = database["todos"]
# user_collection = database["users"]


import motor.motor_asyncio
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
MONGO_DETAILS = os.environ.get("MONGODB_URI")

client = motor.motor_asyncio.AsyncIOMotorClient(
    MONGO_DETAILS,
    tls=True,
    tlsAllowInvalidCertificates=True  # Use this only if you are sure about the server's certificate
)


database = client.Todo

todo_collection = database.get_collection("todos")
user_collection = database.get_collection("users")

def get_todo_collection():
    return todo_collection

def get_user_collection():
    return user_collection


