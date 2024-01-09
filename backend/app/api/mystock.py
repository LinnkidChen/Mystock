from flask import current_app, g, jsonify, request
from flask_httpauth import HTTPBasicAuth
import json

from . import api
from .errors import bad_request, forbidden, unauthorized
import datetime
from werkzeug.utils import secure_filename
import random
from flaskapp import basedir
import base64
import hashlib
import os

@api.route("/test/")
def nihao():
    return "<h1>hello world</h1>"
