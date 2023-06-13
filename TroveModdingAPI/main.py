from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from quart import Quart, jsonify

from api import users_api
from models import User, Profile

api = Quart(__name__)
api.config["SERVER_NAME"] = "slynx.xyz"
api.database_client = None
api.database = None


@api.before_serving
async def start_database():
    api.database_client = AsyncIOMotorClient()
    await init_beanie(api.database_client.tmod_manager, document_models=[User, Profile])
    print("Initialized database!")


@api.route("/", subdomain="tmod")
async def home():
    return "Hello World!"


@api.errorhandler(400)
async def bad_request(e):
    return jsonify({"error": "Bad request"}), 400


if __name__ == "__main__":
    # Register API modules
    api.register_blueprint(users_api)
    # Run API application
    api.run("0.0.0.0", port=18000)
