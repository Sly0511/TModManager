import os
from json import load, dump
from pathlib import Path
from typing import Optional

from flet import ResponsiveRow
from models.trovesaurus.user import User
from pydantic import BaseModel, Field
from utils.api.trovesaurus import query_user
from utils.functions import throttle


class Storage(BaseModel):
    appdata: Path = Path(os.getenv('APPDATA'))

    @property
    def storage_folder(self):
        return self.appdata.joinpath("Sly-Trove")

    @property
    def logs_folder(self):
        return self.storage_folder.joinpath("logs")

    @property
    def mods_folder(self):
        return self.storage_folder.joinpath("mods")

    @property
    def settings_file(self):
        return self.storage_folder.joinpath("settings.json")


class Settings(BaseModel):
    user_token: Optional[str] = None
    theme: str = "DARK"
    color: str = "BLUE"


class Constants(BaseModel):
    storage: Storage = Field(default_factory=Storage)
    user: Optional[User] = None

    @property
    def settings(self) -> Settings:
        if not self.storage.settings_file.exists():
            return Settings()
        return Settings.parse_obj(load(open(self.storage.settings_file)))

    @throttle
    def save_settings(self):
        dump(self.settings, open(self.storage.settings_file, "w+"))

    async def get_user(self):
        if self.settings.user_token is None:
            return self.settings.user_token
        self.user = await query_user(self.settings.user_token)
        return bool(self.user)


class Controller:
    def __init__(self, page):
        self.page = page
        self.interface = ResponsiveRow()
        self.setup_controls()
        self.setup_events()

    def setup_controls(self):
        raise NotImplemented("Please define a setup_controls method before running the controller.")

    def setup_events(self):
        raise NotImplemented("Please define a setup_events method before running the controller.")
