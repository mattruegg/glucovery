import flet as ft
import asyncio
import time


async def main(page: ft.Page):
    chosen_foods = {}
    available_foods = {'apple', 'pear', 'orange', 'kiwi', 'cherry'}

    # FIRST PAGE
    async def start_program(e):
        await page.clean_async()
        await page.add_async(ft.Row([mongo_search, search_mongo_button]))
        await page.add_async(food_dropdown)
        for x in chosen_foods:
            await page.add_async(ft.TextField(label=x, on_change=textbox_results, value=chosen_foods[x]))
            await page.add_async(ft.Slider(min=1, max=5, divisions=4, value=1, label="{value}", data=x, on_change_end=slider_results))
        await page.update_async()

    # SEND MONGO DB SEARCH AND RETRIEVE FOODS
    async def search_for_foods(e):
        search_query = mongo_search
        print(search_query)
        # TODO connect to mongo db

    # CHOOSE A FOOD AND REMOVE IT FROM THE DROPDOWN
    async def choose_food_from_dropdown(e):
        chosen_foods[food_dropdown.value] = ""
        await page.update_async()
        # print(chosen_foods)
        option = await find_option(food_dropdown.value)
        if option != None:
            food_dropdown.options.remove(option)
        await start_program(e)

    async def find_option(option_name):
        for option in food_dropdown.options:
            if option_name == option.key:
                return option
        return None

    # STORE FOOD QUANTITIES
    async def textbox_results(e):
        chosen_foods[e.control.label] = e.control.value
        print(chosen_foods)

    async def slider_results(e):
        # t.value = f"Changed {e.control.data}; slid to {e.control.value}"
        await page.add_async()

    # INITIALIZE VARIABLES
    mongo_search = ft.TextField()
    search_mongo_button = ft.ElevatedButton(
        "Search", on_click=search_for_foods)

    food_dropdown = ft.Dropdown(on_change=choose_food_from_dropdown)
    for x in available_foods:
        food_dropdown.options.append(ft.dropdown.Option(x))

    # SET UP START OF PROGRAM
    await start_program(e=any)
    # start_button = ft.ElevatedButton("Start", on_click=start_program)
    # await page.add_async(start_button)

ft.app(target=main)
