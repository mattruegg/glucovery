import pandas as pd
import os


nutrient_filename = "intake.xlsx"
nutrient_file_path = os.path.join("data", nutrient_filename)
def get_nutrient_intake(age, gender):
    """
    returns the recommended and upper-limit intake for each of the important nutrients

    age: age of the user
    gender: gender of the user, can take on values of "Male" or "Female"

    return: dictionary where key is nutrient name and value is a dictionary of the recommended and upper-limit intake

    """
    if gender == "Female":
        df = pd.read_excel(nutrient_file_path, sheet_name = "Adult Female V2")
    else:
        df = pd.read_excel(nutrient_file_path, sheet_name = "Adult Male V2")
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
    if len(reac_col) == 0 or len(up_col) == 0:
        df = df[["Nutrient", recc_col, up_col]]
        df.columns.values[1] = "RDA"
        df.columns.values[2] = "UL"
        df.set_index("Nutrient", inplace = True)
        res = df.to_dict('index')
    else:
        raise Exception("inputted age outside the boundries of 18-65")
    return res


