from flask import Blueprint


api = Blueprint("api", __name__)

@api.route("/")
def api_entry():
    return "<h1>api entry</h1>"

from . import mystock
# from . import authentication, posts, users, comments, errors

