from pymongo import MongoClient
from pymongo.database import Database
from config import MONGO_CONNECTION_STRING, DB_NAME

client = MongoClient(MONGO_CONNECTION_STRING)[DB_NAME]
def get_db() -> Database:
  return client

