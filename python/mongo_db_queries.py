import pymongo

connection_string = "mongodb+srv://ckalia:ymck-glucovery@cluster0.siiuxrk.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_string)
db = client["glucovery-db"]
collection = db["glucovery-collection"]

# count of documents in collection
collection.count_documents({})
# collection.count_documents({"food_name": food_name_query})

# set queries
food_name_query = "test"
nutrient_name = "Moisture"

# return food from food name 
# TODO - fuzzy search and synonyms, sort results based on score and set limit
# fields returned
fields_returned = ["nutrients"]
res = collection.find(filter = {"food_name": food_name_query}, projection = fields_returned)

# return nutrients from nutrient name
# nutrient_query = {
#     "nutrients": 
#     { "$all": [
#                 {"$elemMatch" : {"Nutrient name": nutrient_name}},
#               ] 
#     }
#     }

nutrient_query = {
    "$or": 
    # insert multiple nutrients that the user is defficient in
    [
        {
            "nutrients": {"$elemMatch" : {"Nutrient name": nutrient_name}}
        }
    ]
    }

res = collection.find(filter = nutrient_query, projection = fields_returned)
