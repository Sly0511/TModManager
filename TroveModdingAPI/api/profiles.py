from models.profile import Profile
from models.user import User
from quart import Blueprint, request, jsonify, abort

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
    profile = await Profile.find_one(
        {
            "owner_token": token,
            "profile_id": profile_id,
            "deleted": False
        }
    )
    if profile is None:
        return abort(404, "Profile doesn't exist")
    # TODO: Handle adding and removing mods from the profile


@profiles_api.route("/delete", methods=["DELETE"])
async def delete_profile():
    token = request.args.get("token")
    profile_id = request.args.get("profile_id")
    if (
        token is None or
        profile_id is None
    ):
        return abort(400)
    profile = await Profile.find_one(
        {
            "owner_token": token,
            "profile_id": profile_id,
            "deleted": False
        }
    )
    if profile is None:
        return abort(404, "Profile doesn't exist")
    profile.deleted = True
    await profile.save()
    return jsonify({"success": "OK", "message": "The profile was deleted."}), 202
