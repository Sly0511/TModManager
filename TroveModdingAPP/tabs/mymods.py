from flet import Tab, icons, Text


class MyMods(Tab):
    def __init__(self, page):
        super().__init__(
            text="My Mods",
            content=Text("Hello"),
            icon=icons.FOLDER_OPEN
        )
