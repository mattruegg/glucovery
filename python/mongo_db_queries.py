import pymongo

connection_string = "mongodb+srv://ckalia:ymck-glucovery@cluster0.siiuxrk.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_string)
db = client["glucovery-db"]
collection = db["glucovery-collection"]

# count of documents in collection
collection.count_documents({})
# collection.count_documents({"food_name": food_name_query})

# set queries
food_name_query = "Apple"
nutrients = ["Ash", "Moisture"]

# return food from food name 
# TODO - fuzzy search and synonyms, sort results based on score and set limit
# fields returned
# fields_returned = ["nutrients"]
# res = collection.find(filter = {"food_name": food_name_query}, projection = fields_returned)
# for obj in res:
#     print(obj)


nutrient_query = {
    # insert multiple nutrients that the user is defficient in
            "nutrients": {"$elemMatch" : {"nutrient_name": {"$in": nutrients}}}
    }

# projection = {
#     # insert multiple nutrients that the user is defficient in
#             "nutrients": {"$elemMatch" : {"Nutrient name": {"$in": nutrients}}},
#             "_id": 0
#     }

# aggregation stuff

group_query = {
    "_id": "$_id",
    "nutrients": {
        "$push": 
            {"nutrient_name": "$nutrients.nutrient_name", "value_100g": "$nutrients.value_100g", "unit": "$nutrients.unit"}
    }
}

pipeline = [
        {"$match": nutrient_query},
        {"$unwind": "$nutrients"},
        {"$match": {"nutrients.nutrient_name": {"$in": nutrients}}},
        {"$group": group_query},
        { "$project": {"_id" : 0, "food_code": 0, "food_weight": 0}}
    ]
q = collection.aggregate(pipeline)
for obj in q:
    print(obj)






# res = collection.find(filter = nutrient_query, projection = {"_id": 0})
# res = collection.find(q)
