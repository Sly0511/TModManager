from flet import (
    AppBar,
    IconButton,
    PopupMenuButton,
    PopupMenuItem,
    Divider,
    Row,
    Text,
    Image,
    AlertDialog,
    TextButton,
    MainAxisAlignment,
    Icon,
    Theme
)
from flet_core.colors import SURFACE_VARIANT
from flet_core.icons import (
    LIGHT_MODE,
    DARK_MODE,
    HOME,
    BUG_REPORT,
    HELP,
    PALETTE,
)


class TroveModManagerAppBar(AppBar):
    def __init__(self, **kwargs):
        self.page = kwargs["page"]
        del kwargs["page"]
        colors = [
            "BLUE",
            "RED",
            "PINK",
            "PURPLE",
            "INDIGO",
            "CYAN",
            "TEAL",
            "GREEN",
            "LIME",
            "YELLOW",
            "AMBER",
            "ORANGE",
            "BROWN",
        ]
        actions = []
        actions.extend(
            [
                IconButton(
                    data="theme_switcher",
                    icon=DARK_MODE if self.page.theme_mode == "LIGHT" else LIGHT_MODE,
                    on_click=self.change_theme,
                    tooltip="Change theme",
                ),
                PopupMenuButton(
                    icon=PALETTE,
                    items=[
                        PopupMenuItem(
                            data=color,
                            content=Row(
                                controls=[
                                    Icon(PALETTE,color=color),
                                    Text(value=" ".join([w.capitalize() for w in color.split("_")]))
                                ]
                            ),
                            on_click=self.change_color
                        )
                        for color in colors
                    ],
                ),
                PopupMenuButton(
                    data="other-buttons",
                    items=[
                        PopupMenuItem(
                            data="discord",
                            content=Row(
                                controls=[
                                    Image(
                                        (
                                            "assets/icons/brands/discord-mark-black.png"
                                            if self.page.theme_mode == "LIGHT"
                                            else "assets/icons/brands/discord-mark-white.png"
                                        ),
                                        width=19,
                                    ),
                                    Text("Discord"),
                                ]
                            ),
                            on_click=self.go_url,
                        ),
                        PopupMenuItem(
                            data="github",
                            content=Row(
                                controls=[
                                    Image(
                                        (
                                            "assets/icons/brands/github-mark-black.png"
                                            if self.page.theme_mode == "LIGHT"
                                            else "assets/icons/brands/github-mark-white.png"
                                        ),
                                        width=19,
                                    ),
                                    Text("Github"),
                                ]
                            ),
                            on_click=self.go_url,
                        ),
                        PopupMenuItem(
                            data="paypal",
                            content=Row(
                                controls=[
                                    Image(
                                        "assets/icons/brands/paypal-mark.png", width=19
                                    ),
                                    Text("Paypal"),
                                ]
                            ),
                            on_click=self.go_url,
                        ),
                        Divider(),
                        PopupMenuItem(
                            icon=BUG_REPORT,
                            data="discord",
                            text="Report a bug",
                            on_click=self.go_url,
                        ),
                        PopupMenuItem(
                            icon=HELP, text="About", on_click=self.open_about
                        ),
                    ],
                    tooltip="Others",
                ),
            ]
        )
        actions.extend(kwargs.get("actions", []))
        super().__init__(
            leading_width=40,
            bgcolor=SURFACE_VARIANT,
            actions=actions,
            center_title=True,
            **kwargs,
        )

    async def change_theme(self, _):
        self.page.theme_mode = "LIGHT" if self.page.theme_mode == "DARK" else "DARK"
        await self.page.client_storage.set_async("theme", self.page.theme_mode)
        for action in self.actions:
            if action.data == "theme_switcher":
                action.icon = (
                    DARK_MODE if self.page.theme_mode == "LIGHT" else LIGHT_MODE
                )
            if action.data == "other-buttons":
                for item in action.items:
                    if item.data in ["discord", "github"] and item.content is not None:
                        item.content.controls[0].src = (
                            f"assets/icons/brands/{item.data}-mark-black.png"
                            if self.page.theme_mode == "LIGHT"
                            else f"assets/icons/brands/{item.data}-mark-white.png"
                        )

        await self.page.update_async()

    async def change_color(self, event):
        color = event.control.data
        self.page.theme = Theme(color_scheme_seed=color)
        await self.page.update_async()

    async def go_url(self, event):
        urls = {
            "discord": "https://discord.gg/duuFEsFWk5",
            "github": "https://github.com/Sly0511/NotYetCreated",
            "paypal": "https://www.paypal.com/paypalme/waterin",
        }
        await self.page.launch_url_async(urls[event.control.data])

    async def open_about(self, event):
        self.dlg = AlertDialog(
            modal=True,
            title=Text("About"),
            actions=[
                TextButton("Close", on_click=self.close_dlg),
            ],
            actions_alignment=MainAxisAlignment.END,
            content=Text(
                "Amazing!"
            ),
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.dialog = self.dlg
        self.dlg.open = True
        await self.page.update_async()

    async def close_dlg(self, e):
        self.dlg.open = False
        await self.page.update_async()
