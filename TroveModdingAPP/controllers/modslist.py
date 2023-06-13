from asyncio import create_task, sleep

from flet import (
    Column,
    DataTable,
    DataColumn,
    DataRow,
    DataCell,
    Text,
    Image,
    ProgressBar,
    Row,
    Icon,
    icons,
    Container,
    Card,
    ResponsiveRow,
    FilledButton,
    padding
)
from models.application import Controller
from utils.api.trovesaurus import get_mods_list
from utils.controls.scrolling import ScrollingFrame
from models.trovesaurus.mods import ModFileType


class ModsListController(Controller):
    def setup_controls(self):
        if not hasattr(self, "selected_mod"):
            self.selected_mod = None
        self.interface.height = self.page.height
        self.interface.controls.clear()
        self.progress = Column(
            controls=[
                Text(f"Loading mods list"),
                ProgressBar(width=300),
            ],
            visible=False,
            col=12
        )
        self.mod_list = DataTable(
            columns=[
                DataColumn(Text('Image')),
                DataColumn(Text('Name')),
                DataColumn(Text('Author(s)')),
                DataColumn(Text('Views')),
                DataColumn(Text('Downloads')),
                DataColumn(Text('Likes')),
            ],
            visible=False,
            col=8
        )
        self.mods_list = ScrollingFrame(
            content=Column(
                controls=[
                    self.progress,
                    Column(
                        controls=[
                            self.mod_list
                        ]
                    )
                ],
            ),
            height=750,
            col=9,
            expand=True
        )
        self.mods_card = Column(
            alignment="center",
            horizontal_alignment="center",
            col=3
        )
        self.interface.controls.append(self.mods_list)
        self.interface.controls.append(self.mods_card)
        create_task(self.load_mods_list())

    def setup_events(self):
        ...

    async def load_mods_list(self, limit=20):
        await sleep(0.1)
        self.mod_list.rows.clear()
        self.progress.visible = True
        self.mod_list.visible = False
        await self.progress.update_async()
        await self.mods_card.update_async()
        for i, mod in enumerate(sorted(await get_mods_list(), key=lambda x: -x.downloads)[:limit]):
            if self.selected_mod is None:
                self.selected_mod = mod
                files = await self.selected_mod.get_files()
                self.selected_file = files[0] if 0 < len(files) else None
                self.mods_card.controls = await self.get_mod_card()
            self.mod_list.rows.append(
                DataRow(
                    data=mod,
                    cells=[
                        DataCell(Column(controls=[Image(src=mod.image_url, width=100)])),
                        DataCell(Text(mod.name)),
                        DataCell(Text(mod.author)),
                        DataCell(Text(f"{mod.views:,}")),
                        DataCell(Text(f"{mod.downloads:,}")),
                        DataCell(Text(f"{mod.likes:,}"))
                    ],
                    selected=mod == self.selected_mod,
                    on_select_changed=self.change_selected_mod
                )
            )
            self.progress.controls[1].value = (i+1)/limit
            await self.progress.update_async()
        self.progress.visible = False
        self.mod_list.visible = True
        await self.progress.update_async()
        await self.mods_card.update_async()
        await self.mod_list.update_async()

    async def change_selected_mod(self, event):
        self.selected_mod = event.control.data
        files = await self.selected_mod.get_files()
        self.selected_file = files[0] if 0 < len(files) else None
        self.mods_card.controls = await self.get_mod_card()
        for row in self.mod_list.rows:
            if row.data == self.selected_mod:
                row.selected = True
            else:
                row.selected = False
        await self.mods_card.update_async()
        await self.mod_list.update_async()

    async def change_selected_file(self, event):
        self.selected_file = event.control.data
        self.mods_card.controls = await self.get_mod_card()
        await self.mods_card.update_async()

    async def get_mod_card(self):
        return [
            Image(src=self.selected_mod.image_url, width=200, height=100),
            Text(self.selected_mod.name, size=18, weight="bold"),
            ResponsiveRow(
                controls=[
                    Row(
                        controls=[
                            Row(
                                controls=[
                                    Icon(icons.REMOVE_RED_EYE, size=13),
                                    Text(f"{self.selected_mod.views:,}")
                                ]
                            ),
                            Row(
                                controls=[
                                    Icon(icons.THUMB_UP, size=13),
                                    Text(f"{self.selected_mod.likes:,}")
                                ]
                            ),
                            Row(
                                controls=[
                                    Icon(icons.DOWNLOAD, size=13),
                                    Text(f"{self.selected_mod.downloads:,}")
                                ]
                            )
                        ],
                        alignment="center"
                    ),
                    *(
                        [
                            Card(
                                Container(
                                    Column(
                                        controls=[
                                            Text("Description:", size=16),
                                            Column(
                                                controls=[
                                                    Text(self.selected_mod.clean_description)
                                                ],
                                                height=150,
                                                scroll="auto"
                                            )
                                        ]
                                    ),
                                    padding=padding.only(top=5, left=10, right=15, bottom=5)
                                )
                            )
                        ] if self.selected_mod.clean_description else []
                    ),
                    Card(
                        Container(
                            ResponsiveRow(
                                controls=[
                                    Text("Versions:"),
                                    ScrollingFrame(
                                        Container(
                                            Row(
                                                controls=[
                                                    FilledButton(
                                                        icon=(
                                                            icons.INSERT_DRIVE_FILE
                                                            if file.type == ModFileType.TMOD else
                                                            (
                                                                icons.FOLDER_ZIP
                                                                if file.type == ModFileType.ZIP else
                                                                icons.SETTINGS_APPLICATIONS
                                                            )
                                                        ),
                                                        data=file,
                                                        text=file.version,
                                                        on_click=self.change_selected_file
                                                    )
                                                    for file in self.selected_mod.file_objs
                                                ]
                                            ),
                                            padding=padding.only(bottom=15)
                                        )
                                    )
                                ]
                            ),
                            padding=padding.only(top=5, left=10, right=15)
                        )
                    ),
                    *(
                        [
                            Card(
                                Container(
                                    Column(
                                        controls=[
                                            Text("Change Log:", size=16),
                                            Column(
                                                controls=[
                                                    Text(self.selected_file.clean_changes)
                                                ],
                                                height=80,
                                                scroll="auto"
                                            )
                                        ]
                                    ),
                                    padding=padding.only(top=5, left=10, right=15, bottom=5)
                                )
                            )
                        ] if self.selected_file.clean_changes else []
                    ),
                    *(
                        [
                            Card(
                                Container(
                                    Column(
                                        controls=[
                                            Text("Replaces:", size=16),
                                            Column(
                                                controls=[
                                                    Text(self.selected_file.clean_replacements)
                                                ],
                                                height=50,
                                                scroll="auto"
                                            )
                                        ]
                                    ),
                                    padding=padding.only(top=5, left=10, right=15, bottom=5)
                                )
                            )
                        ] if self.selected_file.clean_replacements else []
                    )
                ]
            )
        ]

