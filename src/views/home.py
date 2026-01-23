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
        ...

        # Layout
        ...

        self.page.clean()
        self.page.add(...)
