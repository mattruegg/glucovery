import flet as ft
import asyncio
import time


async def main(page: ft.Page):
    nums = [
         ft.dropdown.Option("1"),
         ft.dropdown.Option("2"),
         ft.dropdown.Option("3"),
         ft.dropdown.Option("4"),
         ft.dropdown.Option("5"),
    ]

    t = ft.Text()

    chosen_foods = {}
    available_foods = ['apple', 'pear', 'orange', 'kiwi', 'cherry']

    async def textbox_results(e):
        t.value = f"Typing in {e.control.label}; typed {e.control.value}"
        await page.add_async(t)
    
    async def slider_results(e):
        t.value = f"Changed {e.control.data}; slid to {e.control.value}"
        await page.add_async(t)

    async def start_program(e):
        await page.clean_async()
        await page.add_async(food_dropdown)
        for x in chosen_foods:
            await page.add_async(ft.TextField(label=x, on_change=textbox_results))
            await page.add_async(ft.Slider(min = 1, max = 5, divisions = 4, value = 2, label = "{value}", data = x, on_change_end=slider_results))
        await page.update_async()

    async def find_option(option_name):
        for option in food_dropdown.options:
            if option_name == option.key:
                return option
        return None

    async def choose_food_from_dropdown(e):
        chosen_foods[food_dropdown.value] = 0
        await page.update_async()
        # print(chosen_foods)
        option = await find_option(food_dropdown.value)
        if option != None:
            food_dropdown.options.remove(option)
        await start_program(e)

    food_dropdown = ft.Dropdown(on_change=choose_food_from_dropdown)
    for x in available_foods:
        food_dropdown.options.append(ft.dropdown.Option(x))

    start_button = ft.ElevatedButton("Start", on_click=start_program)
    await page.add_async(start_button)

ft.app(target=main)