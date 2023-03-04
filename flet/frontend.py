import flet as ft
import asyncio
import time


async def main(page: ft.Page):
    chosen_foods = {}
    available_foods = {'apple', 'pear', 'orange', 'kiwi', 'cherry'}
    chosen_symptoms = {}
    available_symptoms = {'headache', 'numbness', 'nausea'}

    # FIRST PAGE
    async def foods_page(e):
        await page.clean_async()
        await page.add_async(ft.Row([mongo_food_search, search_mongo_foods_button]))
        await page.add_async(food_dropdown)
        for x in chosen_foods:
            await page.add_async(ft.TextField(label=x, on_change=textbox_results, value=chosen_foods[x]))
        await page.add_async(go_to_symptoms)
        await page.update_async()

    # SEND MONGO DB SEARCH AND RETRIEVE FOODS
    async def search_for_foods(e):
        search_query = mongo_food_search
        print(search_query)
        # TODO connect to mongo db

    # CHOOSE A FOOD AND REMOVE IT FROM THE DROPDOWN
    async def choose_food_from_dropdown(e):
        chosen_foods[food_dropdown.value] = ""
        await page.update_async()
        option = await find_option(food_dropdown.value)
        if option != None:
            food_dropdown.options.remove(option)
        await foods_page(e)

    async def find_option(option_name):
        for option in food_dropdown.options:
            if option_name == option.key:
                return option
        return None

    # STORE FOOD QUANTITIES
    async def textbox_results(e):
        chosen_foods[e.control.label] = e.control.value
        print(chosen_foods)

    # SECOND PAGE
    async def symptoms_page(e):
        await page.clean_async()
        await page.add_async(ft.Row([mongo_symptom_search, search_mongo_symptoms_button]))
        await page.add_async(symptom_dropdown)
        for x in chosen_symptoms:
            await page.add_async(ft.Row(
                [
                    ft.Text(x),
                    ft.Slider(min=1, max=5, divisions=4, value=chosen_symptoms[x], label="{value}", data=x, on_change_end=slider_results),
                ]
            ))
        await page.update_async()

    # SEND MONGO DB SEARCH AND RETRIEVE SYMPTOMS
    async def search_for_symptoms(e):
        search_query = mongo_symptom_search
        print(search_query)
        # TODO connect to mongo db

    # CHOOSE A SYMPTOM AND REMOVE IT FROM THE DROPDOWN
    async def choose_symptom_from_dropdown(e):
        chosen_symptoms[symptom_dropdown.value] = ""
        await page.update_async()
        option = await find_option(symptom_dropdown.value)
        if option != None:
            symptom_dropdown.options.remove(option)
        await symptoms_page(e)

    async def find_option(option_name):
        for option in symptom_dropdown.options:
            if option_name == option.key:
                return option
        return None
    
    # STORE SYMPTOM VALUES
    async def slider_results(e):
        chosen_symptoms[e.control.data] = e.control.value
        print(chosen_symptoms)

    # INITIALIZE VARIABLES
    mongo_food_search = ft.TextField()
    search_mongo_foods_button = ft.ElevatedButton(
        "Search", on_click=search_for_foods)
    
    mongo_symptom_search = ft.TextField()
    search_mongo_symptoms_button = ft.ElevatedButton(
        "Search", on_click=search_for_symptoms)

    food_dropdown = ft.Dropdown(on_change=choose_food_from_dropdown)
    for x in available_foods:
        food_dropdown.options.append(ft.dropdown.Option(x))
        
    symptom_dropdown = ft.Dropdown(on_change=choose_symptom_from_dropdown)
    for x in available_symptoms:
        symptom_dropdown.options.append(ft.dropdown.Option(x))

    go_to_symptoms = ft.ElevatedButton("Go To Symptoms", on_click=symptoms_page)

    # SET UP START OF PROGRAM
    await foods_page(e=any)
    # start_button = ft.ElevatedButton("Start", on_click=start_program)
    # await page.add_async(start_button)

ft.app(target=main)
