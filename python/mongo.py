import pymongo
import json
from pymongo import MongoClient, InsertOne
import os
# from .upload_gluten_free_foods.upload_mongo import res_dict
import requests
import os
import json

connection_string = "mongodb+srv://ckalia:ymck-glucovery@cluster0.siiuxrk.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_string)
db = client["glucovery-db"]
collection = db["glucovery-cluster"]
requesting = []

food_breakdown_url = "https://food-nutrition.canada.ca/api/canadian-nutrient-file/nutrientamount/?type=json&lang=en"
# nutrient_url = "https://food-nutrition.canada.ca/api/canadian-nutrient-file/nutrientname/"
lang = 'en'
data_type = "json"
context = {"lang": lang, "type": data_type, "id": 4}

# Write CNF json data to disk
file_path = os.path.join("data", "nutrient_amount.json")
res = requests.get(food_breakdown_url, params=context)
if res.ok:
    with open(file_path, 'wb') as file:
        file.write(res.content)


with open(file_path, 'rb') as f:
    myDict = json.load(f)
    for dict in myDict:
        requesting.append(InsertOne(dict))
result = collection.bulk_write(requesting)

# requesting.append(InsertOne(res_dict))

# result = collection.bulk_write(requesting)
client.close()

# filename = r"data/nutrient_amount.json"






