import pprint
from typing import List
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
        ref = client[collections[0]].find_one()['data']
        com = client[collections[1]].find_one()['data']
        new_features = get_new_features_by_attribute(ref, com, 'name')
        changed_features = get_changed_features(ref, com)
        return {"new_features": new_features, "changed_features": changed_features}
    else:
        return {}


def get_changed_features(ref: dict, com: dict) -> List:
    changed_features = []
    for idx, feature in enumerate(ref):
        if (feature in com and ref[idx] != com[idx]):
            changed_features.append(feature['name'])
    return changed_features


def get_new_features_by_attribute(ref: dict, com: dict, attr: str) -> List:
    ref_set = set([x[attr] for x in ref])
    com_set = set([x[attr] for x in com])
    return list(ref_set - com_set)
