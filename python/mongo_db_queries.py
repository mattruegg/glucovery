import pymongo
import time

# view stuff
# can let user select age, name, gender, dietary preferences (checkbox), allergies (checkbox)

connection_string = "mongodb+srv://ckalia:ymck-glucovery@cluster0.siiuxrk.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_string)
db = client["glucovery-db"]
collection = db["glucovery-collection"]

# performs aggregation on nutrient values
def sum_nutrient_values():
    pass

# note: no sorting on score capability with fuzzy match
# limit is limit on results outputted
search_index_name = "default1"
# TODO - can we easily flag an incoming food as unsafe (allergies, contains gluten)
def find_food(search_query, limit):
    """
    returns the nutrition information for foods in a users diet

    search query: search query made by user
    limit: number of search results to return that match

    return: list of dictionaries. each dictionary contains food_weight and nutrients list.

    """
# pipeline - for each space seperated term, matches any substring with 1 character variation
# autocomplete searches substrings as opposed to the whole word
    pipeline = [
        {
            "$search": 
                {
                    "index": search_index_name,
                    "autocomplete": {"query": search_query, "path": "food_name", "fuzzy": {"maxEdits": 1}} 
                }
        },
        {"$unwind": "$nutrients"},
        {"$sum", }
        {"$limit": limit},
        {
            "$project": {
            "_id": 0, "food_weight": 1, "nutrients": 1,
            # "score": { "$meta": "searchScore" }
            }
        },
    ]

    #  pipeline = [
    #         {"$match": {"$and": [nutrient_query, {"is_vegan": is_vegan}, {"is_vegetarian": is_vegetarian}]}},
    #         {"$unwind": "$nutrients"},
    #         {"$match": {"nutrients.nutrient_name": {"$in": nutrients}}},
    #         {"$group": group_query},
    #         { "$project": {"_id" : 0}}
    #     ]


    # start_time = time.time()
    result = collection.aggregate(pipeline)
    # print("--- %s seconds ---" % (time.time() - start_time))
    # explain_output = db.command('aggregate', 'glucovery-collection', pipeline=pipeline, explain=True)
    
    # # print results
    res = []
    for i in result:
        res.append(i)

    return res

a = find_food("frot", 1)
print(a)


nutrients = ["Protein", "Carbohydrate"]
# TODO how to take into account allergens
def get_food_from_nutrients(nutrients, dietary_preferences, allergens):
    """
    returns a list of foods and their nutrients such that atleast one nutrient matches

    nutrients: list of nutrients that aren't being met
    dietary_preferences: list of dietary_preferences for a user
    allergies: list of allergens for a user

    return: list of dictionaries. each dictionary contains food_name, food_weight, and nutrients list.

    """
    is_vegan = dietary_preferences["is_vegan"]
    is_vegetarian = dietary_preferences["is_vegetarian"]

    nutrient_query = {
        # insert multiple nutrients that the user is defficient in
                "nutrients": {"$elemMatch" : {"nutrient_name": {"$in": nutrients}}}
        }

    group_query = {
        "_id": "$_id",
        "food_name": {"$first": "$food_name"},
        "food_weight": {"$first": "$food_weight"},
        "nutrients": {
            "$push": 
                {"nutrient_name": "$nutrients.nutrient_name", "value_100g": "$nutrients.value_100g", "unit": "$nutrients.unit"}
        }
    }

    pipeline = [
            {"$match": {"$and": [nutrient_query, {"is_vegan": is_vegan}, {"is_vegetarian": is_vegetarian}]}},
            {"$unwind": "$nutrients"},
            {"$match": {"nutrients.nutrient_name": {"$in": nutrients}}},
            {"$group": group_query},
            { "$project": {"_id" : 0}}
        ]

    q = collection.aggregate(pipeline)
    res = []
    for obj in q:
        res.append(obj)
    return res

# a = get_food_from_nutrients(nutrients, is_vegan, is_vegetarian)
# print(a)