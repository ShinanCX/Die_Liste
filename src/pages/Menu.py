import flet as ft
from assets.funcs import Settings

class Menu(ft.NavigationDrawer):
    def __init__(self, page: ft.Page, settings: Settings) -> None:
        super().__init__()
        # selected_index 0 = Startseite
        # selected_index 1 = Die Liste
        # selected_index 2 = Einstellungen
        self.selected_index = 0
        self.controls=[
            ft.Container(height=5),
            ft.NavigationDrawerDestination(
                label="Startseite",
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                label="Die Liste",
                icon=ft.Icons.FORMAT_LIST_NUMBERED
            ),
            ft.NavigationDrawerDestination(
                label="Einstellungen",
                icon=ft.Icons.SETTINGS
            )
        ]
        self.on_change=self.navigate

    
    def navigate(self, e):
        if e.control.selected_index == 1:
            self.page.go("/dieliste")
        elif e.control.selected_index == 2:
            self.page.go("/einstellungsseite")