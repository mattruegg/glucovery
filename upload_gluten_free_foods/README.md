# Uploading to MongoDB

## Important Condsiderations
- Before downloading the CNF excel file, choose the serving size `100 grams of edible portion = 100 grams`
- Choose a food name that is simple ex. `apple-fuji-raw-skin` becomes `apple`
- The food weight variable is the estimated average weight in grams of a single unit of the food
- You will be shown a success message if the food uploads successfully
## How to Upload CNF Excel Files to MongoDB
- Download the CNF excel file for the desired food and put it in the `data` directory
- In the `upload_mongo.py` file in the `upload_gluten_free_foods` directory, edit the value for the following  `8` variables:

    - `food_code` ex. 4
    - `food_name` ex. "apple"
    - `food_weight` ex. 250
    - `is_vegetarian` ex. False
    - `is_vegan` ex. False
    - `is_liquid` ex. False
    - `filename` ex. "file.xls"
    - `allergens` 
- Run the `upload_mongo.py` python file to upload the data
