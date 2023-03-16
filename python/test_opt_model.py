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
    return len(missing_nutrients) == 0


def test_correctness(optimized_foods, possible_foods, missing_nutrients):
    print(missing_nutrients)
    # get food information for foods found in optimized foods
    food_information = []
    for possible_food in possible_foods:
        food_name = possible_food["food_name"]
        if food_name in optimized_foods:
            food_quantity = optimized_foods[food_name]
            food_information.append([possible_food, food_quantity])
    # built dict where key is nutrient and amount is value across all foods in optimized foods
    nutrient_amounts = {}
    for food, quantity in food_information:
        food_name = food["food_weight"]
        nutrients = food["nutrients"]
        for nutrient in nutrients:
            nutrient_name = nutrient["nutrient_name"]
            nutrient_value = nutrient["value_100g"]
            if nutrient_name in missing_nutrients:
                nutrient_amounts[nutrient_name] = nutrient_amounts.get(nutrient_name, 0) + get_total_amount(food_name, quantity, nutrient_value)
    print("nutrient_amounts: ", nutrient_amounts)

    # compare summed amounts with rda value for nutrient
    for nutrient_name, nutrient_amount in nutrient_amounts.items():
        nutrient_amount_missing = missing_nutrients[nutrient_name]
        if nutrient_amount_missing - nutrient_amount > 0:
            print(f"Nutrient {nutrient_name} is still not met")
    print("all nutrient amounts are met!")
        

# gets total summed amount given quantity of food in opt amount and adds it to summed_amount in user diet
def get_total_amount(food_name, food_quantity, nutrient_value):
    iron_multiplier = 1.8 if food_name == "Iron, Fe" else 1
    return (food_quantity/ 100) * nutrient_value * iron_multiplier
        
        


def main():
    # initalize input

    dietary_preferences = {"is_vegan": True, "is_vegetarian": True}
    user_information = {"sex": "Male", "age": 19}

    nutrient_intake = RecommendedNutrientIntake()
    rec_nutrient_intake = nutrient_intake.get_nutrient_intake(user_information)

    summed_nutrient_amounts = {"Protein": 40, "Iron, Fe": 6, "Folate, naturally occurring": 400,
                               'Vitamin B-6': 1.3, 'Vitamin B-12': 2.4, 'Vitamin D': 15,'Copper, Cu': 0.9, 
                               'Zinc, Zn':11,'Calcium, Ca': 1000, 'Magnesium, Mg': 400,
                               'Retinol activity equivalents, RAE': 900, 'Tocopherol, alpha': 15,
                               'Vitamin K': 120, 'Potassium, K': 4700, 'Phosphorus, P': 700, 
                               'Sodium, Na': 1500, 'Manganese, Mn': 2.3, 'Selenium, Se':55, 'Carbohydrate': 130, 
                               'Fibre, total dietary': 38}
    
    nutrient_calculations = NutrientCalculations()
    missing_nutrients = nutrient_calculations.determine_missing_nutrient_amounts(summed_nutrient_amounts, rec_nutrient_intake)
    missing_nutrients_list = list(missing_nutrients.keys())
    possible_foods = nutrient_calculations.get_food_from_nutrients(missing_nutrients_list, dietary_preferences)

    # check if foods contain all nutrients
    foods_contain_all_nutrients = check_contain_nutrients(possible_foods, missing_nutrients_list.copy())
    if foods_contain_all_nutrients:
        print("foods do contain all nutrients")
        opt_model = OptModel()
        optimized_foods = opt_model.optimize_food_suggestions(rec_nutrient_intake, summed_nutrient_amounts, possible_foods)
        print("optimized foods: ", optimized_foods)
        return test_correctness(optimized_foods, possible_foods, missing_nutrients)
    else:
        print("no possible foods")
    

main()