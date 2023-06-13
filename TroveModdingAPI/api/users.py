from quart import Blueprint, request, jsonify, abort
from models.user import User


users_api = Blueprint('users', __name__)


@users_api.route("/api/user", subdomain="tmod")
async def get_user():
    token = request.args.get("token", None)
    if token is None:
        return abort(400)
    user = await User.find_one(User.user_token == token)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.json())


@users_api.route("/api/user/create", subdomain="tmod", methods=["PUT"])
async def create_user():
    token = (await request.form).get("token", None)
    if token is None:
        return abort(400)
    user = await User.find_one(User.user_token == token)
    if user is None:
        user = User(user_token=token)
        await user.save()
    return jsonify(user.json())

