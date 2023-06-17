from quart import Blueprint, request, jsonify, abort, current_app
from datetime import datetime

mods_api = Blueprint('mods', __name__, subdomain="tmod", url_prefix="/api/mods")

@mods_api.route("/list")
async def list_mods():
    try:
        last_updated = datetime.utcfromtimestamp(int(request.args["last_updated"]))
        key = request.args.get("key", "totaldownloads")
        reverse = int(request.args.get("reverse", 1))
        start = int(request.args.get("start", 0))
        limit = int(request.args.get("limit", 20))
    except KeyError:
        return abort(400)
    if current_app.mods_last_updated is None:
        return abort(412, "The mods list is compiling, please wait")
    if last_updated >= current_app.mods_last_updated:
        return "The mods list is in sync", 208
    mods_list = sorted(current_app.mods_list, key=lambda x: int(x[key]), reverse=bool(reverse))[start:start+limit]
    return jsonify(mods_list)
