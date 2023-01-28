import pandas as pd
import json
import pymongo
from pymongo import MongoClient, InsertOne
import os

# Add your ip address here: https://cloud.mongodb.com/v2/63cef72751e1dd59e282be0d#/security/network/accessList
# MongoDB Login:
# username: ckalia
# password: ymck-glucovery

food_code = <<FOOD CODE>> 
food_name = "<<SET FOOD NAME>>"
food_weight = <<SET FOOD WEIGHT OF A SINGLE UNIT IN GRAMS>>
filename = "<<SET FILENAME>>"

file_path = os.path.join("data", filename)

# TODO
# remove nutrients that are not needed
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

# remove unncessary columns
n = 3
df.drop(columns=df.columns[-3:], axis=1, inplace=True)

# rename last column (too long)
df.rename(columns={'Value per 100 g of edible portion': 'Value 100g'}, inplace=True)

# remove rows with nutritional value of zero
df = df[df["Value 100g"] != 0]

# remove rows that contain nutrients that aren't of interest to us
# nutrient_order = {"Iron, Fe": 1, "Folic acid, synthetic form": 2, "Vitamin B-6": 3, "Vitamin B-12": 4, "Vitamin D": 5}
# important_nutrients = list(nutrient_order.keys())
# df = df[df['Nutrient name'].isin(important_nutrients)]

# should have 3 columns at this point

# convert df to json
json_str = df.to_json(orient = "records")
lst = json.loads(json_str)

# missing nutrient code unfortunately
res_dict = {"food_code": food_code, "food_name": food_name, "food_weight": food_weight, "nutrients": lst}

# push a single json document to mongodb
connection_string = "mongodb+srv://ckalia:ymck-glucovery@cluster0.siiuxrk.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_string)
db = client["glucovery-db"]
collection = db["glucovery-collection"]

result = collection.insert_one(res_dict)
client.close()