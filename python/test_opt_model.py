# test to see if missing nutrients, summed_nutrient_amounts, rec_intake is same on each run (true)
# test to see if each missing nutrient is contained in atleast one food
# print("missing_nutrients", missing_nutrients)
# print("---")

from mongo_db_queries import NutrientCalculations
from opt_model import OptModel
from reccommended_intake import RecommendedNutrientIntake

def test():
    """
    test to check whether the foods collectively contain the missing nutrients
    and the optimization model can return a result when the foods do
    """
    dietary_preferences = {"is_vegan": True, "is_vegetarian": True}
    user_information = {"sex": "Male", "age": 19}

    missing_nutrients = ["Protein", "Iron, Fe", "Vitamin B-6", "Zinc, Zn"]
    print("missing nutrients: ", missing_nutrients)

    nutrient_intake = RecommendedNutrientIntake()
    rec_nutrient_intake = nutrient_intake.get_nutrient_intake(user_information)

    nutrient_calculations = NutrientCalculations()
    summed_nutrient_amounts = {"Protein": 40, "Iron, Fe": 6, "Vitamin B-6": 1, "Zinc, Zn": 6}
    possible_foods = nutrient_calculations.get_food_from_nutrients(missing_nutrients, dietary_preferences, 10)
    print("number of possible foods", len(possible_foods))

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
    print("are all of the missing nutrients covered: ", len(missing_nutrients) == 0)

    if len(missing_nutrients) == 0:
        opt_model = OptModel()
        optimized_foods = opt_model.optimize_food_suggestions(rec_nutrient_intake, summed_nutrient_amounts, possible_foods)

    
test()
