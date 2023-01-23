import pymongo
import json
from pymongo import MongoClient, InsertOne
import os



client = pymongo.MongoClient("mongodb+srv://ckalia:Bbckkalia11@cluster0.siiuxrk.mongodb.net/?retryWrites=true&w=majority")
db = client["glucovery-db"]
collection = db["glucovery-cluster"]
requesting = []

filename = r"data/nutrient_amount.json"

with open(filename, 'rb') as f:
    myDict = json.load(f)
    for dict in myDict:
        requesting.append(InsertOne(dict))
result = collection.bulk_write(requesting)
client.close()



