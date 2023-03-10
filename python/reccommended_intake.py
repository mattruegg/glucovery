import pandas as pd
import os


class RecommendedNutrientIntake:

    def __init__(this, nutrient_filename = "intake.xlsx"):
        this.nutrient_filename = nutrient_filename,
        this.nutrient_file_path = os.path.join("data", nutrient_filename)

    def get_nutrient_intake(this, user_information):
        """
        returns the recommended and upper-limit intake for each of the important nutrients

        user_information: dictionary containing general information about user

        return: dictionary where key is nutrient name and value is a dictionary of the recommended and upper-limit intake

        """
        sex = user_information["sex"]
        age = user_information["age"]

        if sex == "Female":
            df = pd.read_excel(this.nutrient_file_path, sheet_name = "Adult Female V2")
        else:
            df = pd.read_excel(this.nutrient_file_path, sheet_name = "Adult Male V2")
        
        # get appropriate column name based on user age
        rec_col = ""
        up_col = ""
        if 19 <= age <= 30:
            rec_col = "RDA 19-30"
            up_col = "UL 19-30"
        elif 31 <= age <= 50:
            rec_col = "RDA 31-50"
            up_col = "UL 31-50"
        elif 51 <= age <= 65:
            rec_col = "RDA 51-65"
            up_col = "UL 51-65"
        if len(rec_col) > 0 and len(up_col) > 0:
            df = df[["Nutrient", rec_col, up_col]]
            df.columns.values[1] = "RDA"
            df.columns.values[2] = "UL"
            # remove water
            water_intake = df.loc[df['Nutrient'] == "Water"].to_dict("records")
            df = df[df['Nutrient'] != "Water"]
            df.set_index("Nutrient", inplace = True)
            res = df.to_dict('index')
        else:
            raise Exception("inputted age outside the boundries of 18-65")
        return res
