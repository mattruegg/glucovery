import flet as ft
import asyncio
import time


# async might be a better option for the code
# however I (matt) cannot get it to work
# with views, which I think is necessary
# to make the pages work

# leaving this here in case we want to try
# and come back to it

async def main(page: ft.Page):
    await page.add_async(ft.Text(f"Initial route: {page.route}"))
    await page.add_async(ft.Text("this"))

    async def go_store(e):
        page.route = "/store"
        await page.update_async()

    async def go_park(e):
        page.route = "/park"
        await page.update_async()

    async def route_change(route):
        if page.route == "/store":
            await page.add_async(ft.Text(f"Initial route: {page.route}"))
            await page.clean_async()
            await page.add_async(ft.Text(f"New route: {route}"))
            page.views.append(
                await page.add_async(ft.ElevatedButton("Go to Park", on_click=go_park))
            )

    page.on_route_change = route_change
    # await page.go_async("/")
    await page.add_async(ft.ElevatedButton("Go to park", on_click=go_store))
    await page.update_async()


ft.app(main)
# ft.app(target=main, view=ft.WEB_BROWSER)
