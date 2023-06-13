from datetime import datetime
from random import sample
from string import ascii_letters, digits

from beanie import Document, Indexed
from pydantic import BaseModel, Field


def random_id(k=8):
    return "".join(sample(ascii_letters + digits, k=k))


class Mod(BaseModel):
    mod_id: int
    file_id: int


class Profile(Document):
    name: str
    profile_id: Indexed(str, unique=True) = Field(default_factory=random_id)
    mods: list[Mod] = []
    shared: bool = False
    deleted: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
