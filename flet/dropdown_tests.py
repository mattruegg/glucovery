import flet as ft
import asyncio
import time


def main(page: ft.Page):

    # CREATE FAKE DATA
    data = [
        {
            "name": "john", "age": 12
        },
        {
            "name": "oppw", "age": 12
        },
        {
            "name": "jenifer", "age": 12
        },
        {
            "name": "aaan", "age": 12
        },
        {
            "name": "buyua", "age": 12
        },
        {
            "name": "qwmiu", "age": 12
        },
        {
            "name": "dokoo", "age": 12
        },
        {
            "name": "matt", "age": 12
        },

    ]

    resultdata = ft.ListView()

    resultcon = ft.Container(
        bgcolor="red200",
        content=ft.Column([
            resultdata

        ])
    )


    def searchnow(e):
        mysearch = e.control.value
        result = []

        # IF NOT BLANK YOU TEXTFIELD SEARCH THE RUN FUNCTION
        if not mysearch == "":
            resultcon.visible = True
            for item in data:
                if mysearch in item['name']:
                    result.append(item)
            page.update()

        # IF RESULT THERE DATA THEN PUSH DATA TO WIDGET CONTAINER Resultcon
        if result:
            resultdata.controls.clear()

            def name_select(e):
                resultdata.controls.append(cc.data)
                print(cc.data)

            for x in result:
                # resultdata.controls.append(
                #     # ft.Text(f"name : {x['name']} age : {x['age']}",
                #     #         size=20, color="white"
                #     #         )
                #     ft.ElevatedButton(x['name'], on_click=name_select, data=x)
                # )
                cc = ft.ElevatedButton(x['name'], on_click=name_select, data=x['name'])
                resultdata.controls.append(cc)

            page.update()
        else:
            resultdata.controls.clear()
            page.update()

    # HIDE RESULT FOR YOU SEARCH DEFAULT
    resultcon.visible = False

    txtsearch = ft.TextField(label="Search now",
                             on_change=searchnow
                             )

    page.add(
        ft.Column([
            ft.Text("Search Anything", size=30, weight="bold"),
            txtsearch,
            resultcon
        ])
    )


ft.app(main)
