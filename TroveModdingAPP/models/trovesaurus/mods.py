import re
from base64 import b64encode
from datetime import datetime
from enum import Enum
from typing import Union, Any

from re import compile
from aiohttp import ClientSession
from pydantic import BaseModel, Field, validator


paragraph = compile(r"<p>(.*?)<\/p>")
strong = compile(r"<strong>(.*?)<\/strong>")
img = compile(r"<img.*?>")
anchor = compile(r"<a.*?>(.*?)<\/a>")
ul = compile(r"<ul>(.*?)<\/ul>", re.MULTILINE | re.DOTALL)
li = compile(r"<li>(.*?)</li>")
br = compile(r"<br.*?>")


class ModFileType(Enum):
    TMOD = "tmod"
    ZIP = "zip"
    CONFIG = "config"


class ModFile(BaseModel):
    id: int = Field(alias="modid")
    file_id: int = Field(alias="fileid")
    type: ModFileType = Field(alias="ext")
    is_config: bool = Field(alias="extra")
    version: str
    changes: str
    created_at: Union[int, datetime] = Field(alias="date")
    downloads: int
    name: str = Field(alias="filename")
    size: int = Field(alias="fileid")
    image_url: str = Field(alias="image")
    obsolete: bool
    replacements: str = Field(alias="replaces")

    @validator('created_at')
    def parse_timestamp(cls, value):
        if isinstance(value, datetime):
            return value
        return datetime.utcfromtimestamp(value)

    @validator('obsolete')
    def parse_obsolete(cls, value):
        return bool(int(value))

    @validator('is_config')
    def parse_is_config(cls, value):
        return bool(int(value))

    @validator('version')
    def parse_version(cls, value, values):
        if values["is_config"]:
            return "config"
        if not value.strip():
            return f"File: [{str(values['file_id'])}]"
        return value

    @property
    def clean_changes(self):
        desc = paragraph.sub(r"\1", self.changes)
        desc = strong.sub(r"\1", desc)
        desc = img.sub(r"", desc)
        desc = anchor.sub(r"\1", desc)
        desc = ul.sub(r"", desc)
        desc = br.sub(r"", desc)
        desc = li.sub("\t\u2022 \\1", desc)
        return (
            desc.replace("&nbsp;", "").replace("&gt;", ">").replace("&lt;", "<").strip()
            or None
        )

    @property
    def clean_replacements(self):
        desc = paragraph.sub(r"\1", self.replacements)
        desc = strong.sub(r"\1", desc)
        desc = img.sub(r"", desc)
        desc = anchor.sub(r"\1", desc)
        desc = ul.sub(r"", desc)
        desc = br.sub(r"", desc)
        desc = li.sub("\t\u2022 \\1", desc)
        return (
            desc.replace("&nbsp;", "").replace("&gt;", ">").replace("&lt;", "<").strip()
            or None
        )


class Mod(BaseModel):
    id: int
    name: str
    type: str
    subtype: str
    description: str
    created_at: datetime = Field(alias="date")
    views: int
    replacements: str = Field(alias="replaces")
    downloads: int = Field(alias="totaldownloads")
    thumbnail_url: str = Field(alias="image")
    user_id: int = Field(alias="userid")
    notes: str
    visible: bool
    likes: int = Field(alias="votes")
    author: str
    image_url: str = Field(alias="image_full")
    files_data: Any = Field(alias="downloads")
    file_objs: list[ModFile] = Field(default_factory=list)

    @validator('created_at')
    def parse_timestamp(cls, value):
        if isinstance(value, datetime):
            return value
        return datetime.utcfromtimestamp(value)

    @validator('visible')
    def parse_visible(cls, value):
        return bool(int(value))

    async def get_files(self):
        if self.files_data and not self.file_objs:
            async with ClientSession() as session:
                async with session.get(f"https://trovesaurus.com/client/modfiles.php?modids={self.id}") as response:
                    data = await response.json()
                    files = data[str(self.id)]
                    self.file_objs.extend([ModFile.parse_obj(mf) for mf in files])
        self.file_objs.sort(key=lambda x: -x.file_id)
        return self.file_objs

    @property
    def clean_description(self):
        desc = paragraph.sub(r"\1", self.description)
        desc = strong.sub(r"\1", desc)
        desc = img.sub(r"", desc)
        desc = anchor.sub(r"\1", desc)
        desc = ul.sub(r"", desc)
        desc = br.sub(r"", desc)
        desc = li.sub("\t\u2022 \\1", desc)
        return (
            desc.replace("&nbsp;", "").replace("&gt;", ">").replace("&lt;", "<").strip()
            or None
        )
