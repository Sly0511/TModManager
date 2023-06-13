from aiohttp import ClientSession
from models.trovesaurus.mods import Mod
from pydantic import BaseModel


class Trovesaurus(BaseModel):
    base_url = "https://trovesaurus.com/"
    mods_api = "modsapi"
    mod_files_api = "client/modfiles.php"
    downloads_api = "client/downloadfile.php"
    users_api = "client/useridfromkey.php"


async def query_user(key):
    async with ClientSession as session:
        async with session.get(f"https://trovesaurus.com/client/useridfromkey.php?key={key}") as response:
            if response.status == 200:
                return await response.json()
            else:
                return None


async def get_mods_list():
    async with ClientSession() as session:
        async with session.get("https://trovesaurus.com/modsapi.php?ml=TroveTools.NET&mode=list") as response:
            raw_mods_list = await response.json()
            return [Mod.parse_obj(mod) for mod in raw_mods_list]
