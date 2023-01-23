import requests
import os

# base url
base_url = "https://food-nutrition.canada.ca/api"
# food endpoint
food_url = "canadian-nutrient-file/food/"
# nutrient endpoint
nutrient_url = "https://food-nutrition.canada.ca/api/canadian-nutrient-file/nutrientname/"
food_breakdown_url = "https://food-nutrition.canada.ca/api/drug/nutrientamount/"

lang = 'en'
data_type = "json"
context = {"lang": lang, "type": data_type}

# get particular food using food code
# important features: food name, food description
food_id = "697"
context["id"] = food_id
# res = requests.get(food_url, params = context)
# print(res.text)

# get list of nutrients
# important features: nutrient name, nutrient group
# nutrient_id = "550"
# context["id"] = nutrient_id
res = requests.get(nutrient_url)
print(res.ok)
print(res.text)



# other important endpoints:
# Nutrient Group
# *Nutrient Amount - for a given food, lists the quantity of that nutrient per 100g of that food
# res = requests.get(food_breakdown_url, params = context)
# print(res.text)


# * Serving Size - tells you how to multiply nutrients in a food for a given serving size



