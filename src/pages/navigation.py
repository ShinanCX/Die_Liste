import flet as ft
from pages.Startseite import Startseite
from pages.Einstellungsseite import Einstellungsseite
from pages.Listenseite import Listenseite
from assets.funcs import Settings

def routing(page: ft.Page, settings: Settings) -> dict:
    return {
        "/":ft.View(
            route="/",
            padding=0,
            controls=[
                Startseite(settings, page)
            ]
        ),
        "/einstellungsseite":ft.View(
            route="/einstellungsseite",
            padding=0,
            controls=[
                Einstellungsseite(page, settings)
            ]
        ),
        "/dieliste":ft.View(
            route="/dieliste",
            padding=0,
            controls=[
                Listenseite(page, settings)
            ]
        )
    }