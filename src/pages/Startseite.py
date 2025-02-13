import flet as ft
import random, time
from assets.funcs import Settings


class Startseite(ft.Row):
    def __init__(self, settings: Settings, page: ft.Page) -> None:
        super().__init__()
        self.page = page
        self.data = settings.data
        self.settings = settings.settings
        self.colors = settings.colors
        self.veto_counter = self.settings["people"]
        self.rolled_data = ""
        self.expand=True
        self.game_title_widget = self.game_title()
        self.controls=[
            ft.Container(
                bgcolor=self.colors["creme"],
                expand=True,
                padding=ft.padding.only(top=20, left=20, right=20),
                content=ft.Column(
                    controls=[
                        self.menu(), self.game_title_widget, self.veto_container(), self.buttons()
                    ]
                )
            )
        ]

    def menu(self) -> ft.Row:
        self.menu_widget = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.MENU, 
                    icon_color="black", 
                    icon_size=50,
                    on_click= lambda e: self.page.open(self.page.drawer)),
                ft.Container(
                    margin=ft.margin.only(top=20),
                    alignment=ft.alignment.top_center,
                    content=ft.Text(
                        value="DIE Liste", 
                        size=30, color="black", 
                        text_align=ft.TextAlign.CENTER, 
                        weight=ft.FontWeight.BOLD)),
                ft.IconButton(
                    icon=ft.Icons.POWER_SETTINGS_NEW_OUTLINED, 
                    icon_color="black", 
                    icon_size=50,
                    on_click=lambda close: self.page.window.destroy())
            ]
        )
        return self.menu_widget

    def game_title(self) -> ft.Container:
        self.rolled_data_widget=ft.Text(
                value=self.rolled_data, 
                size=30, color="black", 
                text_align=ft.TextAlign.CENTER)

        self.game_title_widget = ft.Container(
            margin=ft.margin.only(top=200),
            alignment=ft.alignment.center,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        value="Rollergebnis:",
                        color="black",
                        size=25,
                        text_align=ft.TextAlign.CENTER),
                    self.rolled_data_widget
                ]
            )
        )
        return self.game_title_widget

    def veto_container(self) -> ft.Container:
        self.veto_container_widget = ft.Container(
             expand=True,
             alignment=ft.alignment.center
        )
        return self.veto_container_widget

    def roll_button(self) -> ft.FloatingActionButton:
        self.roll_button_widget = ft.FloatingActionButton(
            text="Roll", 
            bgcolor=self.colors["red"],
            expand=True,
            on_click=lambda roll: self.roll()
        )
        return self.roll_button_widget
    
    def veto_button(self) -> ft.FloatingActionButton:
        self.veto_button_widget = ft.FloatingActionButton(
            text=f"Veto [{self.veto_counter}/{self.settings["people"]}]", 
            bgcolor=self.colors["grey"],
            disabled=True,
            expand=True,
            on_click=lambda veto: self.veto()
        )
        return self.veto_button_widget
    
    def buttons(self) -> ft.Container:
        self.buttons_widget = ft.Container(
            alignment=ft.alignment.bottom_center,
            margin=ft.Margin(bottom=30, left=0, right=0, top=0),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    self.roll_button(),
                    ft.VerticalDivider(thickness=10, width=30),
                    self.veto_button()
                ],
            )
        )
        
        return self.buttons_widget
    
    def roll(self) -> None:
        data_list: list = [data for data in self.data]
        if self.settings["weight"]:
            weight_list = []
            for data in self.data:
                weight_list.append(self.data[data]["weight"])
        else:
            weight_list = None
        self.rolled_data = random.choices(data_list, weight_list)[0]

        roll_gif = ft.Image(src="assets\\roll.gif")

        self.veto_container_widget.content=roll_gif
        self.deactivate_button(self.roll_button_widget)
        self.veto_container_widget.update()
        time.sleep(1)
        roll_gif.src="\\assets\\clear.png"
        self.veto_container_widget.update()
        self.activate_button(self.roll_button_widget)
        self.rolled_data_widget.value = self.rolled_data
        self.veto_counter = self.settings["people"]
        self.activate_button(self.veto_button_widget, roll=True)
        self.rolled_data_widget.update()


    def activate_button(self, button: ft.FloatingActionButton, roll=False) -> None:
            if roll:
                button.text = f"Veto [{self.veto_counter}/{self.settings["people"]}]"
            button.disabled=False
            button.bgcolor=self.colors["red"]
            button.update()

    def deactivate_button(self, button: ft.FloatingActionButton) -> None:
            button.disabled=True
            button.bgcolor=self.colors["grey"]
            button.update()

    def veto(self) -> None:
        first_check = random.randint(0, 1)
        second_check = random.randint(0, 1)

        def _handle_veto_related_texts(veto_result: bool) -> None:
            veto_text = ft.Text(
                 value="Veto gestartet",
                 color="black",
                 size=20,
                 text_align=ft.TextAlign.CENTER
            )

            veto_loading_bar = ft.ProgressBar(width=200)

            if self.veto_counter > 0:
                self.veto_counter -= 1
                self.veto_button_widget.text = f"Veto [{self.veto_counter}/{self.settings["people"]}]"
                self.veto_button_widget.update()

            veto_column = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER,
                               controls=[veto_text, veto_loading_bar])

            self.veto_container_widget.content=veto_column
            
            for i in range(0, 51):
                veto_loading_bar.value = i * 0.02
                time.sleep(0.05)
                if veto_loading_bar.value >= 0.5 and first_check == False:
                    veto_text.value="1. Veto Check fehlgeschlagen.."
                    veto_loading_bar.value = 0
                    break
                self.veto_container_widget.update()

            if veto_result:
                veto_text.value="Veto erfolgreich!"
                self.rolled_data_widget.value=""
                self.rolled_data_widget.update()
            elif first_check == True and second_check == False:
                veto_text.value="2. Veto Check fehlgeschlagen.."
            self.veto_container_widget.content=veto_text
            self.veto_container_widget.update()
            time.sleep(2)
            self.veto_container_widget.clean()

        if first_check and second_check:
            veto_result = True
        else:
            veto_result = False
        
        self.deactivate_button(self.veto_button_widget)
        _handle_veto_related_texts(veto_result)
        if not veto_result and self.veto_counter != 0:
            self.activate_button(self.veto_button_widget)