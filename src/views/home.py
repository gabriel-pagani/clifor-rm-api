import flet as ft
from utils.ui import show_message


class HomeView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.codcoligada = str()
        self.customers_vendors = dict()
    
    def show(self):
        def add_cnpj(e):
            ...

        def remove_cnpj(cnpj):
            ...

        def start_automation(e):
            ...

        # Components
        codcoligada_input = ft.Dropdown(
            label="Affiliate",
            options=[
                ft.dropdown.Option("5", "Sinasc"),
                ft.dropdown.Option("6", "ICD"),
                ft.dropdown.Option("1", "BRS"),
            ]
        )

        cnpj_input = ft.TextField(
            label="Cnpj",
            on_submit=add_cnpj,
        )

        ie_input = ft.TextField(
            label="IE",
            on_submit=add_cnpj,
        )

        type_input = ft.Dropdown(
            label="Type",
            options=[
                ft.dropdown.Option("c", "Customer"),
                ft.dropdown.Option("f", "Vendor"),
            ]
        )

        add_cnpj_button = ft.IconButton(
            icon=ft.Icons.ADD,
            icon_size=30,
            tooltip="Add cnpj",
            on_click=add_cnpj,
        )

        remove_cnpj_button = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_size=30,
            tooltip="Remove cnpj",
            on_click=remove_cnpj,
        )

        start_automation_button = ft.Button(
            content="Start automation",
            height=50,
            bgcolor=ft.Colors.GREY_900,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8)
            ),
            on_click=add_cnpj,
        )

        list_of_cnpjs = ...

        logs = ...

        # Layout
        cnpj_form = ft.Row(
            controls=[
                codcoligada_input,
                cnpj_input,
                ie_input,
                type_input,
                add_cnpj_button,
            ]
        )

        column = ft.Column(
            controls=[
                cnpj_form,
                start_automation_button,
            ]
        )

        container = ft.Container(
            content=column,
        )

        self.page.clean()
        self.page.add(container)
