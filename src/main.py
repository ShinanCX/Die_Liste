import flet as ft
from assets.funcs import Settings
from pages.navigation import routing
from pages.Menu import Menu


#available colors: blue, red, orange, yellow, creme

class Applikation():
    def __init__(self, page: ft.Page):
        self.settings = Settings()
        # window config
        window_height = 860
        window_width = 540
        page.window.height = window_height
        page.window.always_on_top = True
        # page.window.min_height = window_height
        # page.window.max_height = window_height
        page.window.width = window_width
        # page.window.min_width = window_width
        # page.window.max_width = window_width

        # page config
        page.bgcolor = self.settings.colors["blue"]
        page.title = "Die Liste!"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.padding=0

        def route_change(route):
            page.views.clear()
            page.views.append(
                routing(page, self.settings)[page.route]
            )
            if page.route == "/":
                page.views[0].drawer = Menu(page, self.settings)
                page.drawer = page.views[0].drawer
            page.update()

        page.on_route_change = route_change
        page.go("/")

if __name__ == "__main__":
    ft.app(target=Applikation)