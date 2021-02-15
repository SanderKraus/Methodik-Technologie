import pprint
from bson.objectid import ObjectId
from pymongo import MongoClient, mongo_client


mongo_client = MongoClient()
client = mongo_client['app-db']


def mongo_insert(collection: str, data: dict) -> ObjectId:
    return client[collection].insert_one(data)


def mongo_get_one(collection: str, query: dict) -> dict:
    return client[collection].find_one(query)


def mongo_delete_collection(collection: str):
    if collection in client.list_collection_names():
        client[collection].drop()


def compare_item_collections() -> dict:
    collections = ['ref_features', 'com_features']
    if all(x in collections for x in client.list_collection_names()):
        ref = client[collections[0]].find_one()
        d = [x['#'] for x in ref['data']]
        print(d)
        com = client[collections[1]].find_one()
        return {}
    else:
        return {}
