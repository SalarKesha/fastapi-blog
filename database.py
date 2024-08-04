from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_USER, MONGO_PASSWORD, MONGO_HOST, MONGO_PORT, MONGO_DATABASE
import pymongo
import asyncio


class MongoDatabase:
    _instance = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(*args, **kwargs)
        return cls._instance

    def __init__(self):
        self.client = AsyncIOMotorClient(f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}")
        self.db = self.client[MONGO_DATABASE]

    @property
    def users(self):
        return self.db['users']

    @property
    def posts(self):
        return self.db['posts']


db = MongoDatabase()
