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
nutrients = ["Moisture", "Ash"]

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
    # insert multiple nutrients that the user is defficient in
            "nutrients": {"$elemMatch" : {"Nutrient name": {"$in": ["Moisture", "Ash"]}}}
    }

# specifies what fields to return
# projection = {
#     "nutrients": 
#     {
#         "$elemMatch": 
#         {
#             "$and":
#             [
#                 {
#                     "Nutrient name": nutrient_name_one
#                 },
#                 {
#                     "Nutrient name": nutrient_name_two
#                 },
#             ]
#         }
#     }, 
#     "_id": False
# }

res = collection.find(filter = nutrient_query, projection = nutrient_query)
for obj in res:
    print(obj)