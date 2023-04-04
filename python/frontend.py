import flet as ft
import math
from mongo_db_queries import NutrientCalculations
import mongo_db_queries as mdq


async def main(page: ft.Page):
    nc = NutrientCalculations()
    chosen_persona = {}
    chosen_symptoms = {}
    available_symptoms = {'headache', 'numbness', 'nausea'}

    chosen_foods = {}

    personas = [{'sex': 'Male', 'age': '28'}, {'sex': 'Female', 'age': '37'}, {
        'sex': 'Female', 'age': '49'}, {'sex': 'Male', 'age': '62'}]
    
    list_of_symptoms = []
    dietary_preferences = {}
    allergens = {}

    profiles_text = ["Profile 1: Sulphite allergy, Vegetarian, Joint Pain and Inflammation",
                      "Profile 2: Egg allergy, Diarrhea and Migraines", "Profile 3: Blank"]

    #
    # --------------------------------------- PERSONAS PAGE ---------------------------------------
    #

    async def personas_page(e):
        await page.clean_async()
        for x in range(3):
            profile = ft.Text(profiles_text[x])
            profile_button = ft.ElevatedButton(
                "Select", on_click=choose_persona, data=x)
            await page.add_async(ft.Row([profile, profile_button]))

    async def choose_persona(e):
        
        nonlocal list_of_symptoms
        nonlocal dietary_preferences
        nonlocal allergens
        nonlocal chosen_foods

        if e.control.data == 0:
            list_of_symptoms = ["Joint Pain", "Inflammation"]
            dietary_preferences = {"is_vegan": False, "is_vegetarian": True}
            allergens = {"Eggs": False, "Milk": False, "Peanuts": False, "Mustard": False, 
                         "Crustaceans and molluscs": False,"Fish": False, "Sesame seeds": False, 
                         "Soy": False, "Sulphites": True, "Tree Nuts": False, "Wheat and triticale": False}
            chosen_foods = {"Cooked Lentils, 1 Cup": 1.5, "Poached Egg": 3, "Sliced Cheddar Cheese": 2, 
                            "Fuji Apple": 2, "Cup of 2% White Milk": 2, "Dried Lychee": 3}
        elif e.control.data == 1:
            list_of_symptoms = ["Diarrhea", "Headache/Migraine"]
            dietary_preferences = {"is_vegan": False, "is_vegetarian": False}
            allergens = {"Eggs": True, "Milk": False, "Peanuts": False, "Mustard": False, 
                         "Crustaceans and molluscs": False,"Fish": False, "Sesame seeds": False, 
                         "Soy": False, "Sulphites": False, "Tree Nuts": False, "Wheat and triticale": False}
            chosen_foods = {"Fuji Apple": 2, "Gala Apple": 2, "Lime": 2, "Cranberry": 3, "Poached Egg": 5,
                    "Cup of 2% White Milk": 2, "Tomato": 5, "Peanut Butter, Natural": 10, "Salmon": 10}
        elif e.control.data == 2:
            list_of_symptoms = []
            dietary_preferences = {"is_vegan": False, "is_vegetarian": False}
            allergens = {"Eggs": False, "Milk": False, "Peanuts": False, "Mustard": False, 
                         "Crustaceans and molluscs": False,"Fish": False, "Sesame seeds": False, 
                         "Soy": False, "Sulphites": False, "Tree Nuts": False, "Wheat and triticale": False}
            chosen_foods = {}
        await foods_page(e=any)

    #
    # --------------------------------------- FOODS PAGE ---------------------------------------
    #

    async def foods_page(e):
        nonlocal chosen_foods
        await page.clean_async()
        await page.add_async(ft.Row([mongo_food_search, search_mongo_foods_button]))
        await page.add_async(food_dropdown)
        lv = ft.ListView(expand=True, spacing=10)
        for x in chosen_foods:
            lv.controls.append(ft.Row(
                [
                    ft.TextField(label=x, on_change=textbox_results,
                                 value=chosen_foods[x]),
                    ft.ElevatedButton("X", on_click=remove_chosen_food, data=x)
                ]
            ))
        await page.add_async(lv)
        await page.add_async(ft.Row([go_to_recommendations, reset_button]))
        await page.update_async()

    # SEND MONGO DB SEARCH AND RETRIEVE FOODS
    async def search_for_foods(e):
        temp = []
        for y in food_dropdown.options:
            temp.append(y)
        for y in temp:
            food_dropdown.options.remove(y)
        search_query = mongo_food_search
        a = nc.search_food_name(search_query.value)
        for x in a:
            food_dropdown.options.append(ft.dropdown.Option(x['food_name']))
        await page.update_async()

    # CHOOSE A FOOD AND REMOVE IT FROM THE DROPDOWN
    async def choose_food_from_dropdown(e):
        chosen_foods[food_dropdown.value] = ""
        await page.update_async()
        option = await find_food_option(food_dropdown.value)
        if option != None:
            food_dropdown.options.remove(option)
        await foods_page(e)

    async def find_food_option(option_name):
        for option in food_dropdown.options:
            if option_name == option.key:
                return option
        return None

    # STORE FOOD QUANTITIES
    async def textbox_results(e):
        chosen_foods[e.control.label] = int(e.control.value)

    # REMOVE CHOSEN FOOD
    async def remove_chosen_food(e):
        chosen_foods.pop(e.control.data)
        food_dropdown.options.append(ft.dropdown.Option(e.control.data))
        await foods_page(e)

    #
    # --------------------------------------- SYMPTOMS PAGE ---------------------------------------
    #

    async def symptoms_page(e):
        await page.clean_async()
        await page.add_async(ft.Row([mongo_symptom_search, search_mongo_symptoms_button]))
        await page.add_async(symptom_dropdown)
        lv = ft.ListView(expand=True, spacing=10)
        for x in chosen_symptoms:
            lv.controls.append(ft.Row(
                [
                    ft.Text(x),
                    ft.Slider(min=1, max=3, divisions=2,
                              value=chosen_symptoms[x], label="{value}", data=x, on_change_end=slider_results),
                    ft.ElevatedButton(
                        "X", on_click=remove_chosen_symptom, data=x)
                ]
            ))
        await page.add_async(lv)
        await page.add_async(ft.Row([go_to_recommendations, reset_button]))
        await page.update_async()

    # SEND MONGO DB SEARCH AND RETRIEVE SYMPTOMS
    async def search_for_symptoms(e):
        search_query = mongo_symptom_search
        # print(search_query)
        # TODO connect to mongo db

    # CHOOSE A SYMPTOM AND REMOVE IT FROM THE DROPDOWN
    async def choose_symptom_from_dropdown(e):
        chosen_symptoms[symptom_dropdown.value] = ""
        await page.update_async()
        option = await find_symptom_option(symptom_dropdown.value)
        if option != None:
            symptom_dropdown.options.remove(option)
        await symptoms_page(e)

    async def find_symptom_option(option_name):
        for option in symptom_dropdown.options:
            if option_name == option.key:
                return option
        return None

    # STORE SYMPTOM VALUES
    async def slider_results(e):
        chosen_symptoms[e.control.data] = e.control.value

    # REMOVE CHOSEN FOOD
    async def remove_chosen_symptom(e):
        chosen_symptoms.pop(e.control.data)
        symptom_dropdown.options.append(ft.dropdown.Option(e.control.data))
        await symptoms_page(e)

    #
    # --------------------------------------- RECOMMENDATIONS PAGE ---------------------------------------
    #
    async def calc_recs(e):
        if len(chosen_foods) == 0:
            await recommendations_page(-4)
            return
        food_recs = mdq.get_food_recs(chosen_foods, list_of_symptoms, dietary_preferences, allergens)
        print(food_recs)
        await recommendations_page(food_recs)

    async def recommendations_page(e):
        await page.clean_async()
        if e == -1:
            await page.add_async(ft.Text("At least one nutrient in your diet exceeds the daily allowance upper limit."))
        elif e == -2:
            await page.add_async(ft.Text("You have met the RDA for all nutrients in your diet."))
        elif e == -3:
            await page.add_async(ft.Text("Foods in database do not contain the nutrients you are deficient in."))
        elif e == -4:
            await page.add_async(ft.Text("Please enter a food."))
        elif len(e) == 0:
            await page.add_async(ft.Text("Recommendation model could not find a suitable set of foods."))
        else:
            for x in e:
                await page.add_async(ft.Text(f"{x}: {(e[x])} servings"))
        await page.add_async(reset_button)

    #
    # --------------------------------------- RESET APPLICATION ---------------------------------------
    #

    async def reset_application(e):
        temp = []
        for y in food_dropdown.options:
            temp.append(y)
        for y in temp:
            food_dropdown.options.remove(y)

        nonlocal list_of_symptoms
        nonlocal dietary_preferences
        nonlocal allergens
        nonlocal chosen_foods

        list_of_symptoms.clear()
        dietary_preferences.clear()
        allergens.clear()
        chosen_foods.clear()
        
        await personas_page(e=any)

    #
    # --------------------------------------- INITIALIZE VARIABLES ---------------------------------------
    #

    mongo_food_search = ft.TextField(on_submit=search_for_foods)
    search_mongo_foods_button = ft.ElevatedButton(
        "Search", on_click=search_for_foods)

    food_dropdown = ft.Dropdown(on_change=choose_food_from_dropdown)

    mongo_symptom_search = ft.TextField()
    search_mongo_symptoms_button = ft.ElevatedButton(
        "Search", on_click=search_for_symptoms)

    symptom_dropdown = ft.Dropdown(on_change=choose_symptom_from_dropdown)
    for x in available_symptoms:
        symptom_dropdown.options.append(ft.dropdown.Option(x))

    go_to_symptoms = ft.ElevatedButton(
        "Go To Symptoms", on_click=symptoms_page)

    go_to_recommendations = ft.ElevatedButton(
        "Calculate Recommendations", on_click=calc_recs)

    reset_button = ft.ElevatedButton("Reset", on_click=reset_application)

    # START PROGRAM
    await personas_page(e=any)

ft.app(target=main)
