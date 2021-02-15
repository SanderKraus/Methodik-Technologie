from bson.objectid import ObjectId
from pymongo import MongoClient


client = MongoClient()


def mongo_insert(collection: str, data: dict) -> ObjectId:
    return client['app-db'][collection].insert_one(data)


def mongo_get_one(collection: str, query: dict) -> dict:
    return client['app-db'][collection].find_one(query)


def mongo_delete_collection(collection: str):
    if collection in client['app-db'].list_collection_names():
        client['app-db'][collection].drop()
