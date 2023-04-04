# test to see if missing nutrients, summed_nutrient_amounts, rec_intake is same on each run (true)
# test to see if each missing nutrient is contained in atleast one food
# print("missing_nutrients", missing_nutrients)
# print("---")
import pandas as pd
from mongo_db_queries import NutrientCalculations
from opt_model import OptModel
from reccommended_intake import RecommendedNutrientIntake

# def check_contain_nutrients(possible_foods, missing_nutrients):
#     """
#     returns true if the foods collectively contain the missing nutrients
#     """

#     for food in possible_foods:
#         if len(missing_nutrients) == 0:
#             break
#         nutrients = food["nutrients"]
#         for nutrient in nutrients:
#             nutrient_name = nutrient["nutrient_name"]
#             nutrient_value = nutrient["value_100g"]
#             if nutrient_name in missing_nutrients:
#                 if nutrient_value > 0:
#                     missing_nutrients.remove(nutrient_name)
#     return len(missing_nutrients) == 0


def test_correctness(optimized_foods, possible_foods, summed_nutrient_amounts, rec_nutrient_intake):
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
        food_name = food["food_name"]
        nutrients = food["nutrients"]
        for nutrient in nutrients:
            nutrient_name = nutrient["nutrient_name"]
            nutrient_value = nutrient["value_100g"]
            nutrient_amounts[nutrient_name] = nutrient_amounts.get(nutrient_name, 0) + get_total_amount(food_name, quantity, nutrient_value)
    print("nutrient_amounts in optimized foods: ", nutrient_amounts)

    # compare summed amounts with rda value for nutrient
    nutrient_amounts_met = True
    for nutrient_name, nutrient_amount in nutrient_amounts.items():
        upper_nutrient_value = rec_nutrient_intake[nutrient_name]["UL"] 
        upper_nutrient = 10000000 if isinstance(upper_nutrient_value, str) else upper_nutrient_value
        lower_nutrient = rec_nutrient_intake[nutrient_name]["RDA"]
        previous_nutrient_amount = summed_nutrient_amounts[nutrient_name]
        new_nutrient_amount = previous_nutrient_amount + nutrient_amount
        if (new_nutrient_amount - lower_nutrient) < -0.1:
            print(f"Nutrient {nutrient_name} is still not met")
            nutrient_amounts_met = False
        elif (previous_nutrient_amount < upper_nutrient) and ((new_nutrient_amount - upper_nutrient) > 0.1):
            print((f"The recommendations brought nutrient {nutrient_name} above the upper limit"))
            nutrient_amounts_met = False
    if nutrient_amounts_met:
        print("all nutrient amounts are met!")
        

# gets total summed amount given quantity of food in opt amount and adds it to summed_amount in user diet
def get_total_amount(food_name, food_quantity, nutrient_value):
    iron_multiplier = 1.8 if food_name == "Iron, Fe" else 1
    return (food_quantity/ 100) * nutrient_value * iron_multiplier

def test_dietary_restrictions(dietary_preferences,possible_foods):
    """
    Checks whether allergens/dietary restrictions were taken into consideration

    """

    user_vegan = dietary_preferences["is_vegan"]
    user_vegetarian = dietary_preferences["is_vegetarian"]

    correct = True
    for food in possible_foods:
        food_vegan = food["is_vegan"]
        food_vegetarian = food["is_vegetarian"]
        food_name = food["food_name"]
        # food_allergen = food["allergens"][allergy]
        if user_vegan:
            if not food_vegan:
                print(f"{food_name} isn't vegan")
                correct = False
        elif user_vegetarian:
            if not food_vegetarian:
                print(f"{food_name} isn't vegetarian")
                correct = False
    if correct:
        return True
    return False

def test_symptoms(list_of_symptoms, possible_foods):
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
        
        for _, row in df.iterrows():
            bad_foods = list(row)[1:]
            for bad_food in bad_foods:
                if bad_food in food_names: 
                    return False
        return True

def test_allergies(user_allergy, possible_foods):
    for food in possible_foods:
        food_allergens = food["allergens"]
        for food_allergen, value in food_allergens.items():
            if food_allergen == user_allergy:
                if value:
                    return False
    return True


def main():
    # initalize input
    dietary_preferences = {"is_vegan": False, "is_vegetarian": False}
    allergens = {"Eggs": True, "Milk": False, "Peanuts": False, "Mustard": False, "Crustaceans and molluscs": False,
        "Fish": False, "Sesame seeds": False, "Soy": False, "Sulphites": False, "Tree Nuts": False, "Wheat and triticale": False
}
    # Testing Purposes
    chosen_allergy = ""
    for allergen in allergens:
        if allergens[allergen]:
            chosen_allergy = allergen      
    
    user_information = {"sex": "Female", "age": 19}

    nutrient_intake = RecommendedNutrientIntake()
    rec_nutrient_intake = nutrient_intake.get_nutrient_intake(user_information)

    # male
    # summed_nutrient_amounts = {"Protein": 36, "Iron, Fe": 20, "Folate, naturally occurring": 400,
    #                            'Vitamin B-6': 1.3, 'Vitamin B-12': 2.4, 'Vitamin D': 15,'Copper, Cu': 0.9, 
    #                            'Zinc, Zn':11,'Calcium, Ca': 1000, 'Magnesium, Mg': 400,
    #                            'Retinol activity equivalents, RAE': 900, 'Tocopherol, alpha': 15,
    #                            'Vitamin K': 120, 'Potassium, K': 4700, 'Phosphorus, P': 700, 
    #                            'Sodium, Na': 1500, 'Manganese, Mn': 2.3, 'Selenium, Se':55, 'Carbohydrate': 130, 
    #                            'Fibre, total dietary': 38}

    # female
    # summed_nutrient_amounts = {'Iron, Fe': 10000, 'Folate, naturally occurring': 400, 'Vitamin B-6': 1.3, 
    #                            'Vitamin B-12': 2.4, 'Vitamin D': 15.0, 'Copper, Cu': 0.9, 'Zinc, Zn': 2.0, 
    #                            'Calcium, Ca': 1000, 'Magnesium, Mg': 310.0, 'Retinol activity equivalents, RAE': 700.0, 
    #                            'Tocopherol, alpha': 15.0, 'Vitamin K': 80.0, 'Potassium, K': 4300.0, 'Phosphorus, P': 700.0, 
    #                            'Sodium, Na': 1500.0, 'Manganese, Mn': 1.8, 'Selenium, Se': 55.0, 'Protein': 46.0, 
    #                            'Carbohydrate': 110.0, 'Fibre, total dietary': 25.0}
    
    nutrient_calculations = NutrientCalculations()
    "---------------------------------------"
    #  if you want to modify foods for testing
    foods_user_ate = {"Fuji Apple": 2 }
    "---------------------------------------"
    foods = nutrient_calculations.find_foods(foods_user_ate)
    summed_nutrient_amounts = nutrient_calculations.sum_nutrient_values(foods, foods_user_ate)
    missing_nutrients = nutrient_calculations.determine_missing_nutrient_amounts(summed_nutrient_amounts, rec_nutrient_intake)
    print("missing nutrients", missing_nutrients)
    missing_nutrients_list = list(missing_nutrients.keys())
    possible_foods = nutrient_calculations.get_food_from_nutrients(missing_nutrients_list, dietary_preferences, allergens)
    print("possible foods: ", len(possible_foods))
    # check if foods contain all nutrients
    foods_contain_all_nutrients = nutrient_calculations.check_contain_nutrients(possible_foods, missing_nutrients_list.copy())
    if foods_contain_all_nutrients:
        print("foods do contain all nutrients")
        print("users dietary restrictions correctly accounted for: ", test_dietary_restrictions(dietary_preferences, possible_foods))
        print("users allergy correctly accounted for: ", test_allergies(chosen_allergy, possible_foods))
        list_of_symptoms = ["Diarrhea", "Headache/Migraine", "Numbness", "Bad Gas"]
        if len(list_of_symptoms) > 0:
            possible_foods = nutrient_calculations.remove_foods(possible_foods, list_of_symptoms)
            print("users symptoms correctly accounted for:", test_symptoms(list_of_symptoms, possible_foods))
        print("number of foods after considering symptoms: ", len(possible_foods))
        opt_model = OptModel()
        optimized_foods = opt_model.optimize_food_suggestions(rec_nutrient_intake, summed_nutrient_amounts, possible_foods)
        print("optimized foods: ", optimized_foods)
        return test_correctness(optimized_foods, possible_foods, summed_nutrient_amounts, rec_nutrient_intake)
    else:
        print("no possible foods")

main()