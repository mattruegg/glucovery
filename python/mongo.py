import pymongo
import json
from pymongo import MongoClient, InsertOne
import os
from .upload_gluten_free_foods.upload_mongo import res_dict

connection_string = "mongodb+srv://ckalia:ymck-glucovery@cluster0.siiuxrk.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_string)
db = client["glucovery-db"]
collection = db["glucovery-cluster"]
requesting = []

requesting.append(InsertOne(res_dict))

result = collection.bulk_write(requesting)
client.close()

# filename = r"data/nutrient_amount.json"

# with open(filename, 'rb') as f:
#     myDict = json.load(f)
#     for dict in myDict:
#         requesting.append(InsertOne(dict))
# result = collection.bulk_write(requesting)
# client.close()





