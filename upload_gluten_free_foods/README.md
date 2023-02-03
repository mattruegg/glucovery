# Uploading to MongoDB

## Important Condsiderations
- Before downloading the CNF excel file, choose the serving size `100 grams of edible portion = 100 grams`
- Choose a food name that is simple ex. `apple-fuji-raw-skin` becomes `apple`
- Don't run the code more than once, it will add a duplicate record
## How to Upload CNF Excel Files to MongoDB
- Login to MongoDB and add your system's IP address:
    - Use the email `ckalia@uwaterloo.ca` and the password `ymck-glucovery` to login to MongoDB
    - Visit this URL: `https://cloud.mongodb.com/v2/63cef72751e1dd59e282be0d#/security/network/accessList`
    - Add your IP address
- Download the CNF excel file for the desired food
- In the `upload_mongo.py` file in the `upload_gluten_free_foods` directory, replace the `<<>>` with a value for the following  `7` variables:

    - `food_code` ex. 4
    - `food_name` ex. "apple"
    - `food_weight` ex. 250
    - `is_vegetarian` ex. False
    - `is_vegan` ex. False
    - `is_liquid` ex. False
    - `filename` ex. "file.xls"
- Run the `upload_mongo.py` python file to upload the data
