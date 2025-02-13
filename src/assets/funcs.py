import json, os, copy
import flet as ft 

# RegEx zum Eintippen von Personenzahlen:
# ^(\d+(-\d+)?)(,(\d+(-\d+)?))*$

class Settings():
    def __init__(self):
        self.file_path: str = os.path.dirname(__file__)
        self.get_colors()
        self.get_settings()
        self.data = self.get_data(self.settings["path"])
       
    def get_colors(self) -> None:
        color_path: str = os.path.join(self.file_path, "../../storage/data/colors.json")

        with open(color_path, mode="r") as json_file:
            self.colors: dict = json.load(json_file)

    def get_settings(self) -> None:
        settings_path: str = os.path.join(self.file_path, "../../storage/data/settings.json")

        with open(settings_path, mode="r") as json_file:
            self.settings: dict = json.load(json_file)

    def get_data(self, data_path) -> dict:
        data_path = data_path
        with open(data_path, mode="r") as json_file:
            data: dict = json.load(json_file)

        if self.settings["reduced"] == True:
            reduced_data: dict = copy.deepcopy(data)
            for data_set in data:
                data_set_ppl_count: str = data[data_set]["peoplecount"]
                data_set_ppl_count_list: list = read_people_count(data_set_ppl_count)
                if self.settings["people"] not in data_set_ppl_count_list:
                    del reduced_data[data_set]
            return reduced_data
        else:
            return data
        
    def update_settings(self, updated_settings: dict) -> None:
        self.settings.update(updated_settings)
        self.data = self.get_data(self.settings["path"])

    def save_files(self, settings=False, data=False):
        files_to_save = []
        dicts_to_save = []
        if settings:
            settings_path = os.path.join(self.file_path, "../../settings.json")
            files_to_save.append(settings_path)
            dicts_to_save.append(self.settings)
        if data:
            data_path = self.settings["path"]
            files_to_save.append(data_path)
            dicts_to_save.append(self.data)

        for i, file in enumerate(files_to_save):
            with open(file, mode="w") as json_file:
                json.dump(dicts_to_save[i], json_file, indent=4)


class Listeneintrag(ft.Container):
    def __init__(self, settings: Settings, entry_name: str, entry_no: int) -> None:
        super().__init__()
        # self.parent_listview = parent
        self.settings = settings
        self.old_entry = {}
        self.new_entry = {}
        self.entry_no = entry_no
        self.entry_name = entry_name
        self.entry_weight = self.settings.data[self.entry_name]["weight"]
        self.entry_ppl_count = self.settings.data[self.entry_name]["peoplecount"]
        self.bgcolor = self.settings.colors["yellow"]
        self.expand = True
        self.border_radius=20
        self.height=110
        self.padding=15
        self.disabled=True
        self.on_click=lambda activate: self.activate_entry()

        self.entry_name_widget = ft.TextField(
            value=self.entry_name,
            color="black",
            disabled=True,
            expand=True,
            content_padding=ft.padding.only(left=0),
            text_style=ft.TextStyle(size=25),
            text_vertical_align=ft.VerticalAlignment.START
        )

        self.entry_weight_widget = ft.TextField(
            value=str(self.entry_weight),
            label="Gewichtung",
            color="black",
            disabled=True,
            label_style=ft.TextStyle(color="black"),
            input_filter=ft.InputFilter(regex_string=r"^\d*(\.)?(\d)?$")
        )

        self.entry_pplcount_widget = ft.TextField(
            value=self.entry_ppl_count,
            label="Personenzahl",
            disabled=True,
            color="black",
            label_style=ft.TextStyle(color="black"),
            input_filter=ft.InputFilter(regex_string=r"^$|^(\d+(-\d*)?)(,(\d+(-\d*)?))*,$|^(\d+(-\d*)?)(,(\d+(-\d*)?))*$")
        )

        self.save_entry_widget = ft.IconButton(
            icon=ft.Icons.SAVE_ALT_OUTLINED,
            icon_color="black",
            visible=False,
            bgcolor=self.settings.colors["red"],
            alignment=ft.alignment.center,
            padding=0,
            tooltip="Speichert die Änderung",
            on_click=lambda deactivate: self.save_entry()
        )

        self.delete_entry_widget = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color="black",
            visible=False,
            bgcolor=self.settings.colors["red"],
            alignment=ft.alignment.center,
            padding=0,
            tooltip="Löscht Eintrag",
            icon_size=27,
            on_click=self.delete_entry
        )

        self.content=ft.Column(
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Row(
                    expand=True,
                    controls=[
                        ft.Text(
                            value=f"{self.entry_no}.",
                            size=20,
                            color="black"),
                        self.entry_name_widget,
                        self.save_entry_widget,
                        self.delete_entry_widget
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    expand=True,
                    controls=[
                        ft.Container(
                            expand=2,
                            alignment=ft.alignment.center_left,
                            padding=ft.padding.only(right=10),
                            content=self.entry_weight_widget),
                        ft.Container(
                            expand=4,
                            alignment=ft.alignment.center_left,
                            content=self.entry_pplcount_widget
                        )
                    ]
                )
            ]
        )

        self.entry_info_widgets = [self.entry_name_widget, self.entry_pplcount_widget, self.entry_weight_widget]


    def activate_entry(self) -> None:
        self.old_entry = {
            self.entry_name_widget.value: {
                "weight": float(self.entry_weight_widget.value), 
                "peoplecount": self.entry_pplcount_widget.value
            }
        }

        self.entry_name_widget.disabled = False
        self.entry_pplcount_widget.disabled = False
        self.entry_weight_widget.disabled = False
        self.save_entry_widget.visible = True
        self.delete_entry_widget.visible = True
        self.update()

    def save_entry(self):
        def _validate_entries() -> None:
            error_message = None

            for entry_info in self.entry_info_widgets:
                if "" == entry_info.value.strip():
                    error_message = "Leere Eingabe!"

            if self.new_entry[self.entry_name_widget.value]["peoplecount"][-1] in [",", "-"]:
                error_message = "Fehlerhafte Personenzahl!"

            if error_message is not None:
                raise KeyError(error_message)



        self.new_entry = {
            self.entry_name_widget.value: {
                "weight": float(self.entry_weight_widget.value), 
                "peoplecount": self.entry_pplcount_widget.value
            }
        }
        try:
            _validate_entries()
        except KeyError as e:
            wrong_entry_alert = ft.AlertDialog(
                    title=ft.Text(value="Achtung"),
                    content=ft.Text(value=str(e) + "\nEintrag wurde nicht geändert."),
                    on_dismiss=lambda close: self.page.close(wrong_entry_alert)
                )

            self.page.open(wrong_entry_alert)
            raise KeyError(str(e))
        
        if self.new_entry == self.old_entry:
            self.deactivate_entry()
            return
        else:
            data_items = list(self.settings.data.items())
            data_keys = list(self.settings.data.keys())
            temp_list = list(self.new_entry.items())
            data_items.pop(self.entry_no - 1)
            data_keys.pop(self.entry_no - 1)

            if self.entry_name_widget.value in data_keys:
                entry_name_exists = ft.AlertDialog(
                    title=ft.Text(value="Achtung"),
                    content=ft.Text(value="Eintrag mit gleichen Namen existiert bereits.\nEintrag wurde nicht geändert."),
                    on_dismiss=lambda close: self.page.close(entry_name_exists)
                )

                self.page.open(entry_name_exists)
                raise KeyError 
    
            data_items.insert(self.entry_no - 1, temp_list[0])
            self.settings.data = dict(data_items)
            self.settings.save_files(data=True)
            self.deactivate_entry()


    def deactivate_entry(self) -> None:
        self.entry_name_widget.disabled = True
        self.entry_pplcount_widget.disabled = True
        self.entry_weight_widget.disabled = True
        self.save_entry_widget.visible = False
        self.delete_entry_widget.visible = False
        self.old_entry = {}
        self.new_entry = {}
        self.update()

    def delete_entry(self, e) -> None:

        delete_entry_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                value="Achtung!"
            ),
            content=ft.Text(
                value="Soll der Eintrag wirklich gelöscht werden?\nDieser Vorgang kann nicht rückgängig gemacht werden!"
            ),
            actions=[
                ft.TextButton(
                    text="Ja",
                    on_click=lambda delete: handle_delete()
                ),
                ft.TextButton(
                    text="Abbrechen",
                    on_click=lambda close: self.page.close(delete_entry_dialog)
                )
            ]
        )

        self.page.open(delete_entry_dialog)

        def handle_delete():
            del self.settings.data[self.entry_name]
            self.page.close(delete_entry_dialog)
            self.parent.controls.remove(self)
            self.parent.update()
            self.settings.save_files(data=True)

def read_people_count(ppl_str: str) -> list:
    splitted_str = ppl_str.split(",")
    people_count_list: list = []
    for entry_ppl_count in splitted_str:
        if entry_ppl_count.isdigit():
            people_count_list.append(int(entry_ppl_count))
        else:
            splitted_sub_str = entry_ppl_count.split("-")
            number_to_add = int(splitted_sub_str[0])
            while number_to_add <= int(splitted_sub_str[1]):
                people_count_list.append(number_to_add)
                number_to_add += 1
    return people_count_list