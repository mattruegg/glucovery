import pymongo
import time
import os
import pandas as pd

from reccommended_intake import get_nutrient_intake

connection_string = "mongodb+srv://ckalia:ymck-glucovery@cluster0.siiuxrk.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_string)
db = client["glucovery-db"]
collection = db["glucovery-collection"]

# performs aggregation on nutrient values
# TODO food quantity would be different for each food
def sum_nutrient_values(foods_list, food_quantity):
    """
    returns the sum of each important nutrient from different foods

    foods_list: list of foods
    # food: a dictionary containing information about a single food from the database
    food_quantity: number of units of the food 

    return: dictionary where key is food name and value is it's value summed up from all foods in user diet

    """
    nutrient_filename = "intake.xlsx"
    nutrient_file_path = os.path.join("data", nutrient_filename)
    df_nutrients = pd.read_excel(nutrient_file_path)

    # keep important nutrients
    nutrient_list = list(df_nutrients["Nutrient"])

    nutrient_values = {}
    nutrient_set = set(nutrient_list)
    for index, food in enumerate(foods_list):
        food_name = food.get("food_name")
        nutrients = food.get("nutrients")
        for nutrient in nutrients:
            nutrient_name = nutrient.get("nutrient_name")
            food_weight = food.get("food_weight")
            nutrient_value = nutrient.get("value_100g")
            # iron is multiplied by 1.8
            iron_multiplier = 1.8 if food_name == "Iron, Fe" else 1
            # this multiplier tells us how much of the nutrient there is in the quantity of the food
            nutrient_multiplier = (food_weight / 100) * food_quantity * iron_multiplier
            nutrient_values[nutrient_name] = nutrient_values.get(nutrient_name, 0) + nutrient_value * nutrient_multiplier
            if index == 0:
                nutrient_set.remove(nutrient_name)
        if index == 0:
            for remaining_nutrient in nutrient_set:
                nutrient_values[remaining_nutrient] = 0
    return nutrient_values

def determine_missing_nutrient_amounts(nutrients_in_diet, recommended_intake):
    """
    returns the nutrients that are missing from the user's diet

    nutrients_in_diet: summed-up amounts for each nutrient in the user's diet
    recommended_intake: recommended intake for each nutrient

    return: dictionary where key is nutrient and value is amount missing based on RDA

    """
    missing_nutrients = {}
    for nutrient, user_intake in nutrients_in_diet.items():
        if nutrient in recommended_intake:
            rec_intake = recommended_intake.get(nutrient).get("RDA")
            up_intake = recommended_intake.get(nutrient).get("UL")
            if user_intake < rec_intake:
                missing_nutrients[nutrient] = rec_intake - user_intake
            # upper limit that doesn't exist, is recored as "ND" in the intake dataset
            elif type(up_intake) in ("int", "float") and user_intake > up_intake:
                raise Exception(f"User's {nutrient} intake exceeds upper limit")
        else:
            missing_nutrients[nutrient] = 0
    return missing_nutrients


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

        {"$limit": limit},
        {
            "$project": {
            "_id": 0, "food_weight": 1, "nutrients": 1,
            # "score": { "$meta": "searchScore" }
            }
        },
    ]

    # start_time = time.time()
    result = collection.aggregate(pipeline)
    # print("--- %s seconds ---" % (time.time() - start_time))
    # explain_output = db.command('aggregate', 'glucovery-collection', pipeline=pipeline, explain=True)
    
    # # print results
    res = []
    for i in result:
        res.append(i)

    return res


# nutrients = ["Protein", "Carbohydrate"]
def get_food_from_nutrients(nutrients, dietary_preferences, allergens = ""):
    """
    returns a list of foods and their nutrients such that atleast one nutrient matches

    nutrients: list of nutrients that aren't being met
    dietary_preferences: dictionary of dietary_preferences for a user
    allergies: list of allergens for a user

    return: list of dictionaries. each dictionary contains food_name, food_weight, and nutrients list.

    """
    is_vegan = dietary_preferences["is_vegan"]
    is_vegetarian = dietary_preferences["is_vegetarian"]

    nutrient_query = {
        # insert multiple nutrients that the user is defficient in
                "nutrients": {"$elemMatch" : {"nutrient_name": {"$in": nutrients}}}
        }

    # allergens_query = {
    #     "allergens": {"$elemMatch": {"allergen_name": }}
    # }

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


def main():
    # for now, I set this value to be 1. However, it would be more.
    a = find_food("Fuji Apple", 1)
    # at this point, they select one food from the returned search results
    b = sum_nutrient_values(a, 2)
    print(b)
    # c = get_nutrient_intake(19)
    # d = determine_missing_nutrient_amounts(b, c)
    # dietary_preferences = {"is_vegan": True, "is_vegetarian": True}
    # missing_nutrients_list = list(d.keys())
    # e = get_food_from_nutrients(missing_nutrients_list, dietary_preferences)
    # return e[0]
print(main())
