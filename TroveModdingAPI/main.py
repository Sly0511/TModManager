from datetime import datetime

from aiohttp import ClientSession
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from quart import Quart, jsonify

from api import users_api, profiles_api, mods_api
from models import User, Profile
from utils import tasks
from utils.functions import chunks

api = Quart(__name__)
api.config["SERVER_NAME"] = "slynx.xyz"
api.database_client = None
api.database = None
api.mods_list = []
api.mods_last_updated = None


@api.before_serving
async def start_database():
    api.database_client = AsyncIOMotorClient()
    await init_beanie(api.database_client.tmod_manager, document_models=[User, Profile])
    print("Initialized database!")
    update_mods_list.start()


@api.route("/", subdomain="tmod")
async def home():
    return "Hello World!"


@api.errorhandler(400)
async def bad_request(e):
    return jsonify(
        {
            "error": "bad_request",
            "message": "Your request wasn't properly formatted for this endpoint."
        }
    ), 400


@api.errorhandler(403)
async def not_authorized(e):
    return jsonify(
        {
            "error": "not_authorized",
            "message": "You don't have access to this resource."
        }
    ), 403


@api.errorhandler(404)
async def not_found(e):
    return jsonify(
        {
            "error": "not_found",
            "message": e.description
        }
    ), 404


@api.errorhandler(412)
async def too_early(e):
    return jsonify(
        {
            "error": "precondition_failed",
            "message": e.description
        }
    ), 412


@tasks.loop(seconds=300)
async def update_mods_list():
    api.mods_list.clear()
    async with ClientSession() as session:
        async with session.get("https://trovesaurus.com/modsapi.php?ml=TroveTools.NET&mode=list") as response:
            api.mods_list.extend(await response.json())
    mods_ids = ",".join([mod["id"] for mod in api.mods_list])
    async with ClientSession() as session:
        async with session.post(f"https://trovesaurus.com/client/modfiles.php", data={"ModIDs": mods_ids}) as response:
            try:
                data = await response.json()
                for key, value in data.items():
                    for mod in api.mods_list:
                        if mod["id"] == key:
                            mod["file_objs"] = value
            except Exception as e:
                print(e.__class__)
    api.mods_last_updated = datetime.utcnow()
    print("Updated Mods list")


@update_mods_list.before_loop
async def before_update_mods_list():
    print("Fetching mods list")


if __name__ == "__main__":
    # Register API modules
    api.register_blueprint(users_api)
    api.register_blueprint(profiles_api)
    api.register_blueprint(mods_api)
    # Run API application
    api.run("0.0.0.0", port=80, debug=True)
