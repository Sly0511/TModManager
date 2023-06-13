from quart import Blueprint, request, jsonify, abort
from models.user import User
from aiohttp import ClientSession


users_api = Blueprint('users', __name__, subdomain="tmod", url_prefix="/api/user")


@users_api.route("/get")
async def get_user():
    token = request.args.get("token", None)
    if token is None:
        return abort(400)
    user = await User.find_one(User.user_token == token, fetch_links=True)
    if user is None:
        return abort(404, "User not found")
    return jsonify(user.json())


@users_api.route("/create", methods=["POST"])
async def create_user():
    token = request.args.get("token", None)
    if token is None:
        return abort(400)
    async with ClientSession() as session:
        async with session.get(f"https://trovesaurus.com/client/useridfromkey.php?key={token}") as response:
            if response.status != 200:
                return abort(400)
    user = await User.find_one(User.user_token == token)
    if user is None:
        user = User(user_token=token)
        await user.save()
    return jsonify(user.json())

