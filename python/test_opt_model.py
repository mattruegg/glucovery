# test to see if missing nutrients, summed_nutrient_amounts, rec_intake is same on each run (true)
# test to see if each missing nutrient is contained in atleast one food
# print("missing_nutrients", missing_nutrients)
# print("---")

from mongo_db_queries import NutrientCalculations
from opt_model import OptModel
from reccommended_intake import RecommendedNutrientIntake

def check_contain_nutrients(possible_foods, missing_nutrients):
    """
    returns true if the foods collectively contain the missing nutrients
    """

    for food in possible_foods:
        # lst = []
        if len(missing_nutrients) == 0:
            break
        nutrients = food["nutrients"]
        for nutrient in nutrients:
            nutrient_name = nutrient["nutrient_name"]
            nutrient_value = nutrient["value_100g"]
            if nutrient_name in missing_nutrients:
                if nutrient_value > 0:
                    missing_nutrients.remove(nutrient_name)
    print(len(missing_nutrients) == 0)


def test_correctness(optimized_foods, possible_foods, missing_nutirents):
    # get food information for foods found in optimized foods
    food_information = []
    for possible_food in possible_foods:
        food_name = possible_food["food_name"]
        if food_name in optimized_foods:
            food_information.append(possible_food)
    # built dict where key is nutrient and amount is value across all foods in optimized foods
    nutrient_amounts = {}
    for food in food_information:
        nutrients = food["nutrients"]
        for nutrient in nutrients:
            nutrient_name = nutrient["nutrient_name"]
            if nutrient_name in missing_nutirents:
                nutrient_amounts[nutrient_name] = get_total_amount()

    # compare summed amounts with rda value for nutrient
    for nutrient_name, nutrient_amount in nutrient_amounts.keys():
        nutrient_amount_missing = missing_nutirents[nutrient_name]
        if nutrient_amount_missing - nutrient_amount > 0:
            print(f"Nutrient {nutrient_name} is still not met")
    print("all nutrient amounts are met!!")
        

# gets total summed amount given quantity of food in opt amount and adds it to summed_amount in user diet
def get_total_amount():
    pass
        
        


def main():
    # initalize input

    dietary_preferences = {"is_vegan": True, "is_vegetarian": True}
    user_information = {"sex": "Male", "age": 19}

    nutrient_intake = RecommendedNutrientIntake()
    rec_nutrient_intake = nutrient_intake.get_nutrient_intake(user_information)

    missing_nutrients = ["Protein", "Iron, Fe", "Vitamin B-6", "Zinc, Zn"]
    summed_nutrient_amounts = {"Protein": 40, "Iron, Fe": 6, "Vitamin B-6": 1, "Zinc, Zn": 6}
    nutrient_calculations = NutrientCalculations()
    possible_foods = nutrient_calculations.get_food_from_nutrients(missing_nutrients, dietary_preferences, 10)

    # check if foods contain all nutrients
    foods_contain_all_nutrients = check_contain_nutrients()
    if foods_contain_all_nutrients:
        opt_model = OptModel()
        optimized_foods = opt_model.optimize_food_suggestions(rec_nutrient_intake, summed_nutrient_amounts, possible_foods)
