import flet as ft
import time


def main(page: ft.Page):
    page.title = "Flet testing"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(
        value="0", text_align=ft.TextAlign.CENTER, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    # r = ft.Row(
    #     [
    #         ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
    #         txt_number,
    #         ft.IconButton(ft.icons.ADD, on_click=plus_click),
    #     ],
    #     alignment=ft.MainAxisAlignment.CENTER,
    # )
    # page.add(r)

    def add_clicked(e):
        page.add(ft.Checkbox(label=new_task.value))
        new_task.value = ""
        new_task.focus()
        new_task.update()

    new_task = ft.TextField(hint_text="Whats needs to be done?", width=300)
    button1 = ft.ElevatedButton("Add", on_click=add_clicked)
    page.add(ft.Row([new_task, button1]))


ft.app(target=main)
# ft.app(target=main, view=ft.WEB_BROWSER)
