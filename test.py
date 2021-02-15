from pymongo import MongoClient

client = MongoClient()
print(client.server_info())
