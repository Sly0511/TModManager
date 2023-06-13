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


if __name__ == "__main__":
    # Register API modules
    api.register_blueprint(users_api)
    # Run API application
    api.run("0.0.0.0", port=18000)
