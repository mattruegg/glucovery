import pymongo
import time
import os
import pandas as pd

from opt_model import OptModel
from reccommended_intake import RecommendedNutrientIntake

connection_string = "mongodb+srv://ckalia:ymck-glucovery@cluster0.siiuxrk.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_string)
db = client["glucovery-db"]
collection = db["glucovery-collection"]

class NutrientCalculations:

    def __init__(this):
        this.important_nutrients = {'Iron, Fe', 'Folate, naturally occurring', 'Vitamin B-6', 'Vitamin B-12', 'Vitamin D', 'Copper, Cu', 'Zinc, Zn', 'Calcium, Ca', 'Magnesium, Mg', 'Retinol activity equivalents, RAE', 'Tocopherol, alpha', 'Vitamin K', 'Potassium, K', 'Phosphorus, P', 'Sodium, Na', 'Manganese, Mn', 'Selenium, Se', 'Protein', 'Carbohydrate', 'Fibre, total dietary'}
        this.search_index_name ="default1"

    # note: no sorting on score capability with fuzzy match
    # TODO - can we easily flag an incoming food as unsafe (allergies, contains gluten)
    def search_food_name(this, search_query, limit = 5):
        """
        returns the nutrition information for foods in a users diet

        search query: search query made by user
        limit: number of search results to return that match
        get_nutrients: True if we want to return nutrients else False

        return: list of dictionaries. each dictionary contains food_weight and nutrients list.

        """
    # pipeline - for each space seperated term, matches any substring with 1 character variation
    # autocomplete searches substrings as opposed to the whole word

        projection = {"_id": 0, "food_name": 1, "food_weight": 1, "nutrients": 1}

        pipeline = [
            {
                "$search": 
                    {
                        "index": this.search_index_name,
                        "autocomplete": {"query": search_query, "path": "food_name", "fuzzy": {"maxEdits": 1}} 
                    }
            },

            {"$limit": limit},
            {
                "$project": projection
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


     # TODO create index on food name
    def find_foods(this, foods):
        """
        foods: name of food and quantity that user selects
        returns all food-related information about the foods passed in
        """
        res = []
        for food_name in foods.keys():
            food = collection.find({"food_name": food_name})
            # get food information from MongoDB cursor
            res.append(food[0])
        return res

    def sum_nutrient_values(this, foods, foods_quantities):
        """
        returns the sum of each important nutrient from different foods

        foods: list where each item is a food and all it's information
        foods_quantities: dictionary where key is food name and value is quantity that the user ate

        return: dictionary where key is food name and value is it's value summed up from all foods in user diet

        """

        nutrient_values = {}
        nutrient_set = this.important_nutrients
        for index, food in enumerate(foods):
            food_name = food.get("food_name")
            food_quantity = foods_quantities[food_name]
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

    #TODO handle case when nutrient exceeds upper limit, right now raises Exception
    def determine_missing_nutrient_amounts(this, nutrients_in_diet, recommended_intake):
        """
        returns the nutrients that are missing from the user's diet

        nutrients_in_diet: summed-up amounts for each nutrient in the user's diet
        recommended_intake: recommended intake for each nutrient

        return: dictionary where key is nutrient and value is amount missing based on RDA

        """
        missing_nutrients = {}
        for nutrient, user_intake in nutrients_in_diet.items():
                rec_intake = recommended_intake.get(nutrient).get("RDA")
                up_intake = recommended_intake.get(nutrient).get("UL")
                if user_intake < rec_intake:
                    missing_nutrients[nutrient] = rec_intake - user_intake
                # upper limit that doesn't exist, is recored as "ND" in the intake dataset
                elif type(up_intake) in ("int", "float") and user_intake > up_intake:
                    raise Exception(f"User's {nutrient} intake exceeds upper limit")
        return missing_nutrients


    # nutrients = ["Protein", "Carbohydrate"]
    def get_food_from_nutrients(this, nutrients, dietary_preferences, allergens):
        """
        returns a list of foods and their nutrients such that atleast one nutrient matches

        nutrients: list of nutrients that are missing from user's diet
        dietary_preferences: dictionary of dietary_preferences for a user
        limit: limit on results returned
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
            "is_vegan": {"$first": "$is_vegan"},
            "is_vegetarian": {"$first": "$is_vegetarian"},
            "nutrients": {
                "$push": 
                    {"nutrient_name": "$nutrients.nutrient_name", "value_100g": "$nutrients.value_100g", "unit": "$nutrients.unit"}
            },
            # "allergens": {
            #     "$push": 
            #         {"nutrient_name": "$nutrients.nutrient_name", "value_100g": "$nutrients.value_100g", "unit": "$nutrients.unit"}
            # }
        }

        #  # allergens
        # allergies = []
        # for i in allergens:
        #     if allergens[i]:
        #         allergies.append(i)

        # key = f"allergens.{allergies[0]}"

        # allergens_query = {
        #     # "allergens": {"$elemMatch": {"$and": [{"$in": allergies}, {"$eq": False}]}}
        #     key: { "$eq": False}

        # }

        # dietary preferences
        match_query = []
        match_query.append(nutrient_query)
        # if len(allergies) > 0:
        #     match_query.append(allergens_query)
        if is_vegan or is_vegetarian:
            if is_vegan:
                match_query.append({"is_vegan": is_vegan})
            else:
                match_query.append({"is_vegetarian": is_vegetarian})


        pipeline = [
                {"$match": {"$and": match_query}},
                {"$unwind": "$nutrients"},
                {"$group": group_query},
                { "$project": {"_id" : 0}},
                # {"$limit": limit}
            ]

        q = collection.aggregate(pipeline)
        res = []
        for obj in q:
            res.append(obj)
        return res
        
    def remove_foods(this, possible_foods, list_of_symptoms):

        # df = pd.read_excel("data/symptoms.xlsx", sheet_name="Copy of Bad Foods")
        # df.to_pickle("data/symptoms.pk1")
        '''
        list_of_symptoms: list of names of symptoms user has
        possible_foods: list of possible foods
        
        returns an array of foods that are not bad for symptoms that the user has
        '''
        df = pd.read_pickle("data/symptoms.pk1")

        # use the isin() method to create a boolean mask
        mask = df.isin(list_of_symptoms).any(axis=1)

        # use the boolean mask to remove rows that don't contain those symptoms
        df = df[mask]

        # add food names to a set
        food_names = set()
        for food in possible_foods:
            food_name = food["food_name"]
            food_names.add(food_name)
        
        # get set of foods to remove from possible foods
        foods_to_remove = set()
        for index, row in df.iterrows():
            # get the values of the columns in the row as a list
            bad_foods = list(row)[1:]
            for bad_food in bad_foods:
                if bad_food in food_names: 
                    foods_to_remove.add(food_name)
        
        good_foods = []
        for i, food in enumerate(possible_foods):
            food_name = food["food_name"]
            if food_name not in foods_to_remove:
                good_foods.append(food)
        
        return good_foods     



def get_food_recs(foods_user_ate):
    # create instance of class
    nutrient_calculations = NutrientCalculations()
    # searching for foods by name
    # nutrient_calculations.search_food_name("Fuji Apple")
    
    # example of foods that user selected that they ate
    # foods_user_ate = {"Fuji Apple": 2, "Gala Apple": 2, "Lime": 2, "Cranberry": 3, "Poached Egg": 5, 
    #                 "Cup of 2% White Milk": 2, "Tomato": 5,"Peanut Butter, Natural": 10 }
    foods = nutrient_calculations.find_foods(foods_user_ate)
    summed_nutrient_amounts = nutrient_calculations.sum_nutrient_values(foods, foods_user_ate)
    user_information = {"sex": "Male", "age": 19}
    # create an object of the class RecommendedNutientIntake
    nutrient_intake = RecommendedNutrientIntake()
    rec_nutrient_intake = nutrient_intake.get_nutrient_intake(user_information)
    missing_nutrients = nutrient_calculations.determine_missing_nutrient_amounts(summed_nutrient_amounts, rec_nutrient_intake)
    dietary_preferences = {"is_vegan": False, "is_vegetarian": False}
    allergens = {"Eggs": False, "Milk": False, "Peanuts": False, "Mustard": False, "Crustaceans and molluscs": False,
            "Fish": False, "Sesame seeds": False, "Soy": False, "Sulphites": False, "Tree Nuts": False, "Wheat and triticale": False
    }
    missing_nutrients_list = list(missing_nutrients.keys())
    print("missing nutrients: ", missing_nutrients_list)
    print("number of missing nutrients: ", len(missing_nutrients))
    # limit_on_rec_foods = 90
    # different set of foods can be returned everytime. not necessairly the same everytime
    # TODO not using how much is missing currently
    possible_foods = nutrient_calculations.get_food_from_nutrients(missing_nutrients_list, dietary_preferences, allergens)
    print("number of possible foods: ", len(possible_foods))

    list_of_symptoms = ["Diarrhea", "Headache/Migraine"]
    good_foods = nutrient_calculations.remove_foods(possible_foods, list_of_symptoms)
    print("number of foods after considering symptoms: ", len(good_foods))
    # create an object of the class OptModel
    optimization_model = OptModel()
    optimized_foods = optimization_model.optimize_food_suggestions(rec_nutrient_intake, summed_nutrient_amounts, good_foods)
    # print(optimized_foods)
    return optimized_foods
