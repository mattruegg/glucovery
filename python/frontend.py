import flet as ft
import asyncio
import time
from mongo_db_queries import NutrientCalculations


async def main(page: ft.Page):
    nc = NutrientCalculations()
    chosen_persona = {}
    chosen_foods = {}
    chosen_symptoms = {}
    available_symptoms = {'headache', 'numbness', 'nausea'}

    personas = [{'sex': 'Male', 'age': '28'}, {'sex': 'Female', 'age': '37'}, {
        'sex': 'Female', 'age': '49'}, {'sex': 'Male', 'age': '62'}]

    #
    # --------------------------------------- PERSONAS PAGE ---------------------------------------
    #

    async def personas_page(e):
        await page.clean_async()
        for x in personas:
            profile = ft.Text(f"Sex: {x['sex']}, Age: {x['age']}")
            profile_button = ft.ElevatedButton(
                "Select", on_click=choose_persona, data=x)
            await page.add_async(ft.Row([profile, profile_button]))

    async def choose_persona(e):
        chosen_persona = e.control.data
        await foods_page(e=any)

    #
    # --------------------------------------- FOODS PAGE ---------------------------------------
    #

    async def foods_page(e):
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
        await page.add_async(ft.Row([go_to_symptoms, reset_button]))
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
        chosen_foods[e.control.label] = e.control.value
        # print(chosen_foods)

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
        await page.add_async(ft.Row([go_to_symptoms, reset_button]))
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

    async def recommendations_page(e):
        return

    #
    # --------------------------------------- RESET APPLICATION ---------------------------------------
    #

    async def reset_application(e):
        temp = []
        for y in food_dropdown.options:
            temp.append(y)
        for y in temp:
            food_dropdown.options.remove(y)

        chosen_foods.clear()
        chosen_symptoms.clear()
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
        "Go To Recommendations", on_click=recommendations_page)

    reset_button = ft.ElevatedButton("Reset", on_click=reset_application)

    # START PROGRAM
    await personas_page(e=any)

ft.app(target=main)
