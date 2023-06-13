from quart import Blueprint, request, jsonify, abort
from models.user import User
from models.profile import Profile, Mod
from aiohttp import ClientSession


profiles_api = Blueprint('profiles', __name__, subdomain="tmod", url_prefix="/api/profile")


@profiles_api.route("/create", methods=['POST'])
async def create_profile():
    token = request.args.get("token")
    name = request.args.get("name")
    mods = request.args.get("mods")
    shared = request.args.get("shared")
    if token is None or name is None:
        return abort(400)
    user = await User.find_one(User.user_token == token, fetch_links=True)
    if user is None:
        return abort(404, "User not found")
    profile = Profile(
        name=name,
        mods=mods,
        shared=shared
    )
    await profile.save()
    user.profiles.append(profile)
    await user.save()
    return jsonify(profile.json())


@profiles_api.route("/update", methods=["PATCH"])
async def update_profile():
    token = request.args.get("token")
    profile_id = request.args.get("profile_id")
    added = request.args.get("added")
    removed = request.args.get("removed")
    if (
            token is None or
            profile_id is None or
            (not added and not removed)
    ):
        return abort(400)
    user = await User.find_one(User.user_token == token, fetch_links=True)
    if user is None:
        return abort(404, "User not found")
    profile = None
    for user_profile in user.profiles:
        if user_profile.profile_id == profile_id:
            profile = user_profile
    if profile is None:
        return jsonify()
