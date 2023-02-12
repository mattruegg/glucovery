import pymongo
import time

connection_string = "mongodb+srv://ckalia:ymck-glucovery@cluster0.siiuxrk.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_string)
db = client["glucovery-db"]
collection = db["glucovery-collection"]

# count of documents in collection
collection.count_documents({})
# collection.count_documents({"food_name": food_name_query})

# set queries
food_name_query = "Apple"
# nutrients = ["Ash", "Moisture"]
nutrients = ["Protein", "Carbohydrate"]

##### First CASE

# return food from food name 
# TODO - fuzzy search and synonyms, sort results based on score and set limit
# fields returned
fields_returned = ["nutrients"]
# res = collection.find(filter = {"food_name": food_name_query}, projection = fields_returned)

# define pipeline
# autocomplete - for each space seperated term, matches any substring with 1 character variation
# text - would not allow for substring matches

index = "default1"
food_query = "apple"
limit = 20
pipeline = [
    {
        "$search": 
            {
                "index": index,
                "autocomplete": {"query": food_query, "path": "food_name", "fuzzy": {"maxEdits": 1}}
            }
    },
    {"$limit": limit},
    {
        "$project": {
        "_id": 0, "food_weight": 1, "nutrients": 1,
        # "score": { "$meta": "searchScore" }
        }
    },
]
# run pipeline
# start_time = time.time()
# result = collection.aggregate(pipeline)
# print("--- %s seconds ---" % (time.time() - start_time))
# explain_output = db.command('aggregate', 'glucovery-collection', pipeline=pipeline, explain=True)
# print(explain_output.keys())
# # print results
# res = []
# for i in result:
#     res.append(i)
# print(res)


##### Second CASE

nutrient_query = {
    # insert multiple nutrients that the user is defficient in
            "nutrients": {"$elemMatch" : {"nutrient_name": {"$in": nutrients}}}
    }

# aggregation stuff

group_query = {
    "_id": "$_id",
    "nutrients": {
        "$push": 
            {"nutrient_name": "$nutrients.nutrient_name", "value_100g": "$nutrients.value_100g", "unit": "$nutrients.unit"}
    }
}

# person specific
is_vegan = False
is_vegetarian = False

pipeline = [
        {"$match": {"$and": [nutrient_query, {"is_vegan": is_vegan}, {"is_vegetarian": is_vegetarian}]}},
        {"$unwind": "$nutrients"},
        {"$match": {"nutrients.nutrient_name": {"$in": nutrients}}},
        {"$group": group_query},
        { "$project": {"_id" : 0, "food_code": 0, "food_weight": 0}}
    ]

start_time = time.time()
q = collection.aggregate(pipeline)
print("--- %s seconds ---" % (time.time() - start_time))
# res = []
# for obj in q:
#     print(obj)
#     res.append(obj)
# print(res)






# res = collection.find(filter = nutrient_query, projection = {"_id": 0})
# res = collection.find(q)
