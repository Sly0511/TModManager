from datetime import datetime
from enum import Enum
from pathlib import Path
from random import sample
from string import ascii_letters, digits

from beanie import Document, Indexed
from pydantic import BaseModel, Field


def random_id(k=8):
    return "".join(sample(ascii_letters + digits, k=k))


class GameServer(Enum):
    LIVE = "live"
    PTS = "pts"


class TrovesaurusMod(BaseModel):
    mod_id: int
    file_id: int
    cfg_content: str
    cfg_hash: str
    cfg_last_sync: datetime = Field(default_factory=datetime.utcnow)


class CustomMod(BaseModel):
    hash: str
    name: str
    cfg_content: str
    cfg_hash: str
    cfg_last_sync: datetime = Field(default_factory=datetime.utcnow)


class Profile(Document):
    name: str
    owner_token: str
    profile_id: Indexed(str, unique=True) = Field(default_factory=random_id)
    servers: list[GameServer] = []
    mods: list[TrovesaurusMod, CustomMod] = []
    custom_mods: list[Path] = []
    shared: bool = False
    deleted: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
