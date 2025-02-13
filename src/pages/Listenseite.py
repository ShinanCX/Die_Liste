import flet as ft
import copy
from assets.funcs import Settings, Listeneintrag, read_people_count


class Listenseite(ft.Row):
    def __init__(self, page: ft.Page, settings: Settings) -> None:
        super().__init__()
        self.colors: dict = settings.colors
        self.page = page
        self.edit_mode_toggled = False
        self.settings: Settings = settings
        self.data: dict = settings.data
        self.expand = True
        self.controls = [
            ft.Container(
                bgcolor=self.colors["creme"],
                expand=True,
                padding = ft.padding.only(top=20, left=20, right=20),
                content=ft.Column(
                    controls=[
                        self.title(), 
                        self.list_container(), 
                        self.buttons()
                    ]
                )
            )
        ]

    def title(self) -> ft.Row:
        self.edit_mode_icon = ft.IconButton(
            icon=ft.Icons.EDIT,
            tooltip="Editieren deaktiviert",
            icon_color="black",
            disabled=True,
            bgcolor=None,
            icon_size=25,
            padding=0
        )

        self.title_widget = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Stack(
                    expand=True,
                    alignment=ft.alignment.center,
                    controls=[
                        ft.Container(
                            alignment=ft.alignment.top_center,
                            content=ft.Text(
                                value="Listenübersicht", 
                                size=30,
                                color="black",
                                text_align=ft.TextAlign.CENTER
                            )
                        ),
                        ft.Container(
                            left=0,
                            width=50,
                            height=50,
                            alignment=ft.alignment.center,
                            content=self.edit_mode_icon,
                        ),
                        ft.Container(
                            right=0,
                            width=50,
                            height=50,
                            alignment=ft.alignment.top_right,
                            content=ft.IconButton(
                                icon=ft.Icons.CANCEL_OUTLINED,
                                padding=0,
                                icon_color="black", 
                                icon_size=50,
                                on_click=lambda e: self.page.go("/"),
                            )
                        )
                    ] 
                )
            ]
        )
        return self.title_widget
    
    def list_container(self) -> ft.Container:
        self.list_container_widget = ft.Container(
            bgcolor=self.colors["blue"],
            expand=True,
            border_radius=30,
            margin=ft.margin.only(bottom=20),
            content=self.list_entries())
        return self.list_container_widget

    def list_entries(self) -> ft.ListView:
        self.list_view_widget = ft.ListView(
            expand=True, 
            spacing=10,
            padding=20)

        for i, entry in enumerate(self.data):
            self.list_view_widget.controls.append(Listeneintrag(self.settings, entry, i+1))
            self.page.update()

        return self.list_view_widget

    def add_button(self) -> ft.FloatingActionButton:
        self.add_button_widget = ft.FloatingActionButton(
            text="Add",
            icon=ft.Icons.ADD,
            bgcolor=self.colors["red"], 
            width=self.page.window.width / 2.5,
            on_click=lambda add: self.add_entry_dialog())
        return self.add_button_widget
    
    def edit_button(self) -> ft.FloatingActionButton:
        self.edit_button_widget = ft.FloatingActionButton(
            text="Edit",
            icon=ft.Icons.EDIT,
            bgcolor=self.colors["red"],
            width=self.page.window.width / 2.5,
            on_click=lambda edit: self.open_edit_mode())
        return self.edit_button_widget
    
    def buttons(self) -> ft.Container:
        self.buttons_widget = ft.Container(
            alignment=ft.alignment.bottom_center,
            padding=ft.padding.only(bottom=30),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                expand=True,
                controls=[
                    self.add_button(), self.edit_button()
                ]
            )
        )
        
        return self.buttons_widget
    
    def add_entry_dialog(self, inputs=("", "", "")) -> None:
        new_entry_name = ft.TextField(
            label="Name des Eintrags",
            value=inputs[0]
        )
        new_entry_weight = ft.TextField(
            label="Gewichtung",
            value=inputs[1],
            input_filter=ft.InputFilter(regex_string=r"^\d*(\.)?(\d)?$") 
        )
        new_entry_ppl_count = ft.TextField(
            label="Personenzahl",
            value=inputs[2],
            input_filter=ft.InputFilter(regex_string=r"^$|^(\d+(-\d*)?)(,(\d+(-\d*)?))*,$|^(\d+(-\d*)?)(,(\d+(-\d*)?))*$")
        )
    
        new_entry_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                value="Neuer Eintrag"
            ),
            content=ft.Container(
                height=200,
                width=400,
                content=ft.Column(
                    controls=[
                        new_entry_name,
                        new_entry_weight,
                        new_entry_ppl_count
                    ]
                )
            ),
            actions=[
                ft.TextButton(
                    text="Eintragen",
                    on_click=lambda add: add_entry()
                ),
                ft.TextButton(
                    text="Abbrechen",
                    on_click=lambda close: self.page.close(new_entry_dialog)
                )
            ]
        )

        self.page.open(new_entry_dialog)

        def validate_entries() -> tuple[str, bool]:
            if "" in [entry.strip() for entry in [new_entry_name.value, new_entry_ppl_count.value, new_entry_weight.value]]:
                return ("Eingabe fehlt", False)
            elif new_entry_ppl_count.value[-1] in [",", "-"]:
                return ("Fehlerhafte Personenzahl", False)
            dict_to_add = {
                new_entry_name.value: {
                    "weight": float(new_entry_weight.value),
                    "peoplecount": new_entry_ppl_count.value
                }
            }

            is_new_entry = False

            temp_full_dict: dict = copy.deepcopy(self.data)
            temp_full_dict.update(dict_to_add)

            if len(temp_full_dict) == len(self.data):
                pass
            else:
                self.data.update(dict_to_add)
                is_new_entry = True
            return ("Eintrag existiert bereits", is_new_entry)     

        def add_entry():
            len_actual_data = len(self.data) + 1
            entry = validate_entries()
            if entry[1]:
                self.settings.save_files(data=True)
                if self.settings.settings["people"] in read_people_count(new_entry_ppl_count.value) or not self.settings.settings["reduced"]:
                    self.list_view_widget.controls.append(Listeneintrag(self.settings, new_entry_name.value, len_actual_data))
                    self.list_view_widget.update()
                self.page.close(new_entry_dialog)
            else:
                failed_entry = ft.AlertDialog(
                    title=ft.Text(value="Achtung"),
                    on_dismiss=lambda reset: self.page.open(new_entry_dialog),
                    content=ft.Text(
                        value=f"{entry[0]}.\nEintrag wurde nicht angelegt"
                    )
                )
                self.page.open(failed_entry)
    
    def open_edit_mode(self) -> None:
        if self.edit_mode_toggled:
            try:
                for entry in self.list_view_widget.controls:
                    entry.save_entry()
                    entry.disabled=self.edit_mode_toggled

                self.edit_mode_toggled = False
                self.edit_mode_icon.tooltip = "Editieren deaktiviert"
                self.edit_mode_icon.bgcolor = self.colors["creme"]
                self.edit_mode_icon.icon_color = "black"
            except KeyError as e:
                return
        else:
            for entry in self.list_view_widget.controls:
                entry.disabled=self.edit_mode_toggled

            self.edit_mode_toggled = True

            self.edit_mode_icon.tooltip = "Editieren aktiviert"
            self.edit_mode_icon.bgcolor = "black"
            self.edit_mode_icon.icon_color = "white"

        self.list_view_widget.update()
        self.edit_mode_icon.update()
