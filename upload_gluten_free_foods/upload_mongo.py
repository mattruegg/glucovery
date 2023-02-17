import pandas as pd
import json
import pymongo
from pymongo import MongoClient, InsertOne
import os

## CHANGE THESE VALUES
food_code = 49
food_name = "frog"
# no need to convert to grams i.e.leave it in the units found in CNF
food_weight = 100
# is_vegetarian = False
# is_vegan = False
# is_liquid = False
filename = "nutrient_profile.xls"

file_path = os.path.join("data", filename)

# TODO
# remove duplicate transactions
# be able to add liquids, is_liquid bool field

# read in excel file
n = 4
df = pd.read_excel(file_path, skiprows = n)

# Dropping last n rows using drop
n = 4
df.drop(df.tail(n).index,
        inplace = True)

# remove sub-titles
sub_titles = ["Proximates", "Other Carbohydrates", "Minerals", "Vitamins", "Amino Acids", "Lipids", "Other components"]
df = df[~df['Nutrient name'].isin(sub_titles)]

# remove unncessary columns (only applies for excel file for '100g edible portion' serving)
n = 3
df.drop(columns=df.columns[-3:], axis=1, inplace=True)

# rename columns to remove space-sperated terms
df.rename(columns={'Value per 100 g of edible portion': 'value_100g', "Nutrient name": "nutrient_name", "Unit": "unit"}, inplace=True)

# remove rows with nutritional value of zero
# df = df[df["value_100g"] != 0]

nutrient_filename = "intake.xlsx"
nutrient_file_path = os.path.join("data", nutrient_filename)
df_nutrients = pd.read_excel(nutrient_file_path)

# keep important nutrients
nutrient_list = list(df_nutrients["Nutrient"])
df = df[df['nutrient_name'].isin(nutrient_list)]

# should have 3 columns at this point

# convert df to json
json_str = df.to_json(orient = "records")
lst = json.loads(json_str)

sample_list = [
        {"nutrient_name": "Moisture", "value_100g": 23, "unit": "g"},
        {"nutrient_name": "Ash", "value_100g": 15, "unit": "g"}
]


# missing nutrient code unfortunately
res_dict = {
        "food_code": food_code, 
        "food_name": food_name, 
        "food_weight": food_weight, 
        # "is_vegetarian": is_vegetarian,
        # "is_vegan": is_vegan,
        # "is_liquid": is_liquid,
        "nutrients": sample_list
}

# push a single json document to mongodb
connection_string = "mongodb+srv://ckalia:ymck-glucovery@cluster0.siiuxrk.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_string)
db = client["glucovery-db"]
collection = db["glucovery-collection"]

result = collection.insert_one(res_dict)
client.close()