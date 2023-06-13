from flet import Tab, icons, Text
from controllers import ModsListController


class ModsList(Tab):
    def __init__(self, page):
        ctrl = ModsListController(page)
        super().__init__(
            text="Mods List",
            content=ctrl.interface,
            icon=icons.FOLDER_OPEN
        )
