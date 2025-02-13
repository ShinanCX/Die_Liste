import flet as ft
import copy, os, json
from assets.funcs import Settings


class Einstellungsseite(ft.Row):
    def __init__(self, page: ft.Page, settings: Settings) -> None:
        super().__init__()
        self.setting_object = settings
        self.settings = settings.settings
        self.temp_settings = copy.deepcopy(self.settings)
        self.page = page
        self.colors = settings.colors
        self.changed = False
        self.expand=True
        self.controls=[
            ft.Container(
                bgcolor=self.colors["creme"],
                expand=True,
                padding = ft.padding.only(top=20, left=20, right=20),
                content=ft.Column(
                    controls=[
                        self.title(), 
                        ft.Divider(thickness=2), 
                        self.path_input(), 
                        self.ppl_input(), 
                        self.weight_switch(),
                        self.reduced_switch(),
                        self.save_button()
                    ]
                )
            )
        ]

    def title(self) -> ft.Row:
        self.title_widget = ft.Row(
            controls=[
                ft.Stack(
                    expand=True,
                    alignment=ft.alignment.center,
                    controls=[
                        ft.Container(
                            alignment=ft.alignment.top_center,
                            expand=True,
                            content=ft.Text(
                                value="Einstellungen", 
                                size=30, 
                                color="black", 
                                text_align=ft.TextAlign.CENTER
                            ),
                        ),
                        ft.Container(
                            alignment=ft.alignment.top_right,
                            content=ft.IconButton(
                                icon=ft.Icons.CANCEL_OUTLINED,
                                padding=0,
                                icon_color="black", 
                                icon_size=50,
                                on_click=lambda e: self.handle_quit(),
                            )
                        )
                    ] 
                )
            ]
        )
        return self.title_widget
    
    def path_input(self) -> ft.Container:
        self.file_picker = ft.FilePicker(on_result=self.pick_file)
        self.page.overlay.append(self.file_picker)
        self.page.update()

        self.file_picker_button = ft.IconButton(
            icon=ft.Icons.UPLOAD_FILE,
            icon_color="black",
            on_click=lambda click: self.file_picker.pick_files(
                dialog_title="Wähle Listendatei",
                allow_multiple=False,
                allowed_extensions=["json"],
                initial_directory=os.path.join(__file__, "../"))
        )

        self.path_input_field = ft.TextField(
            label="Pfadangabe zur Liste", 
            value=self.settings["path"], 
            color="black",
            expand=True,
            label_style=ft.TextStyle(color="black"),
            on_change=lambda change: self.handle_change("path", self.path_input_field.value)
        )

        self.path_input_widget = ft.Container(
            padding=ft.padding.only(top=20),
            content=ft.Row(
                controls=[
                    self.path_input_field,
                    self.file_picker_button
                ]
            )
        )
        return self.path_input_widget
    
    def ppl_input(self) -> ft.Container:    
        self.ppl_input_field = ft.TextField(
            label="Personenanzahl",
            value=self.settings["people"],
            color="black",
            label_style=ft.TextStyle(color="black"),
            width=150,
            input_filter=ft.NumbersOnlyInputFilter(),
            on_change=lambda change: self.handle_change("people", self.ppl_input_field.value),
            on_blur=lambda check: check_for_empty_input()
        )

        def check_for_empty_input() -> None:
            if self.ppl_input_field.value == "":
                self.ppl_input_field.value = "1"
                self.ppl_input_field.update()
        
        self.ppl_input_widget = ft.Container(
            content=ft.Row(
                controls=[
                    self.ppl_input_field,
                    ft.IconButton(
                        icon=ft.Icons.ADD_CIRCLE_OUTLINE, 
                        icon_color="black",
                        on_click=lambda plus: self.plus()
                    ),
                    ft.IconButton(
                        icon=ft.Icons.REMOVE_CIRCLE_OUTLINE, 
                        icon_color="black",
                        on_click=lambda minus: self.minus()
                    )
                ]
            )
        )
        return self.ppl_input_widget

    def weight_switch(self) -> ft.Row:
        self.weight_switch_control = ft.Switch(
            label="Gewichtung", 
            value=self.settings["weight"],
            label_style=ft.TextStyle(color="black"),
            on_change=lambda change: self.handle_change("weight", self.weight_switch_control.value)
        )

        self.weight_switch_widget = ft.Row(
            controls=[
                self.weight_switch_control
            ]
        )
        return self.weight_switch_widget
    
    def reduced_switch(self) -> ft.Row:
        self.reduced_switch_control = ft.Switch(
                    label="Liste auf Personenanzahl reduziert",
                    value=self.settings["reduced"],
                    label_style=ft.TextStyle(color="black"),
                    on_change=lambda change: self.handle_change("reduced", self.reduced_switch_control.value)
        )
        self.reduced_switch_widget = ft.Row(
            controls=[
                self.reduced_switch_control
            ]
        )
        return self.reduced_switch_widget

    def save_button(self) -> ft.Container:
        self.save_button_widget = ft.Container(
            expand=True,
            alignment=ft.alignment.bottom_center,
            padding=50,
            content=ft.FloatingActionButton(
                text="Speichern",
                bgcolor=self.colors["red"],
                expand=True,
                width=self.page.window.width,
                on_click=lambda save: self.save()
            )
        )
        return self.save_button_widget
    
    def handle_change(self, changed_setting, setting_value) -> None:
        if changed_setting == "people":
            if setting_value.isdigit():
                setting_value = int(setting_value)
            else:
                setting_value = setting_value
        changed_setting_dict: dict = {changed_setting: setting_value}
        self.temp_settings.update(changed_setting_dict)

    def save(self) -> None:
        try:
            with open(self.temp_settings["path"], mode="r") as file:
                file.close()
            self.setting_object.update_settings(self.temp_settings)
            self.setting_object.save_files(settings=True)
        except FileNotFoundError:
            self.page.open(ft.AlertDialog(
                on_dismiss=self.path_input_field.focus(),
                title=ft.Text(
                    value="Error"),
                content=ft.Text(
                        value="Die eingegebene Datei kann nicht gefunden werden!"
                    )
            ))

    def handle_quit(self):
        if self.temp_settings != self.settings:
            self.page.open(ft.AlertDialog(
                modal=True,
                title=ft.Text(
                    value="Achtung"
                ),
                content=ft.Text(
                    value="Die Einstellungen wurden geändert ohne zu speichern! \nSoll gesichert werden?"
                ),
                actions=[
                    ft.TextButton(
                        text="Ja",
                        on_click=lambda save: self.save_n_quit()
                    ),
                    ft.TextButton(
                        text="Nein",
                        on_click=lambda close: self.page.go("/")
                    )
                ]
            ))
        else:
            self.page.go("/")

    def pick_file(self, e: ft.FilePickerResultEvent):
        self.path_input_field.value = "".join(map(lambda f: f.path, e.files)) if e.files else self.settings["path"]
        self.handle_change("path", self.path_input_field.value)
        self.path_input_field.update()

    def save_n_quit(self):
        self.save()
        self.page.go("/")
    
    def minus(self):
        if int(self.ppl_input_field.value) > 1:
            self.ppl_input_field.value = str(int(self.ppl_input_field.value) - 1)
            self.handle_change("people", self.ppl_input_field.value)
            self.ppl_input_field.update()
    
    def plus(self):
            self.ppl_input_field.value = str(int(self.ppl_input_field.value) + 1)
            self.handle_change("people", self.ppl_input_field.value)
            self.ppl_input_field.update()