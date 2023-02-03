import pandas as pd
import os

age = 19

nutrient_filename = "intake.xlsx"
nutrient_file_path = os.path.join("data", nutrient_filename)
df = pd.read_excel(nutrient_file_path)

age_ranges = ["19-30", "31-50", "51-65"]

# get appropriate column name based on user age
reac_col = ""
up_col = ""
if 19 <= age <= 30:
    recc_col = "RDA 19-30"
    up_col = "UL 19-30"
elif 31 <= age <= 50:
    recc_col = "RDA 31-50"
    up_col = "UL 31-50"
elif 51 <= age <= 65:
    recc_col = "RDA 51-65"
    up_col = "UL 51-65"
# keep only the necessary columns
df = df[["Nutrient", recc_col, up_col]]
res = df.to_dict('records')
