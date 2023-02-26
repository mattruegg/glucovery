import flet as ft
import asyncio
import time


def main(page: ft.Page):
    page.title = "Routes Example"

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Flet app"),
                              bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.ElevatedButton(
                        "Visit Store", on_click=lambda _: page.go("/store")),
                    ft.ElevatedButton(
                        "Go to Park", on_click=lambda _: page.go("/park")),
                ],
                aaa = ft.TextField(label="Hello!"),
            )
        )
        if page.route == "/store":
            page.views.append(
                ft.View(
                    "/store",
                    [
                        ft.AppBar(title=ft.Text("Store"),
                                  bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton(
                            "Go Home", on_click=lambda _: page.go("/")),
                        ft.ElevatedButton(
                            "Go to Park", on_click=lambda _: page.go("/park")),
                    ],
                )
            )
        if page.route == "/park":
            page.views.append(
                ft.View(
                    "/park",
                    [
                        ft.AppBar(title=ft.Text("Park"),
                                  bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton(
                            "Go Home", on_click=lambda _: page.go("/")),
                        ft.ElevatedButton(
                            "Visit Store", on_click=lambda _: page.go("/store")),
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(main)
# ft.app(target=main, view=ft.WEB_BROWSER)
