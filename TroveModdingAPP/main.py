from flet import app, Page, Tabs
from models.application import Constants

from tabs import MyMods, ModsList
from utils.controls.appbar import TroveModManagerAppBar


class ModManager:
    page: Page

    def run(self):
        app(
            target=self.start,
            assets_dir="assets"
        )

    async def start(self, page: Page, restart=False):
        if not restart:
            self.page = page
            page.constants = Constants()
            page.title = "Trove Mod Manager"
            page.padding = 0
            page.window_min_width = page.window_width = 1600
            page.window_min_height = page.window_height = 900
            await self.login()
        page.appbar = TroveModManagerAppBar(page=page)
        tabs = Tabs(
            tabs=[
                MyMods(page),
                ModsList(page)
            ],
            selected_index=1
        )
        await page.add_async(tabs)

    async def login(self):
        ...


if __name__ == '__main__':
    application = ModManager()
    application.run()
