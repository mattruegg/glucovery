from opt_model import food_info, missing_nutrients
# test to see if missing nutrients, summed_nutrient_amounts, rec_intake is same on each run (true)
# test to see if each missing nutrient is contained in atleast one food
print("missing_nutrients", missing_nutrients)
print("---")

lst_of_lsts = []
for food in food_info:
    # lst = []
    if len(missing_nutrients) == 0:
        break
    nutrients = food["nutrients"]
    for nutrient in nutrients:
        nutrient_name = nutrient["nutrient_name"]
        # lst.append(nutrient_name)
    # print("list of nutrients", lst)
    # lst_of_lsts.append(lst)
        if nutrient_name in missing_nutrients:
            missing_nutrients.remove(nutrient_name)
print("are all of the missing nutrients covered: ", len(missing_nutrients) == 0)
