import os

# noinspection PyUnresolvedReferences
from flask import Flask, Blueprint, current_app, send_file

from flask_restplus import Api

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.static_folder = os.path.join(app.config["DIST_DIR"], "static")


# noinspection PyUnusedLocal
@app.route('/', defaults={'path': ''})
@app.route('/<path>/')
def index(path):
    dist_dir = current_app.config["DIST_DIR"]
    entry = os.path.join(dist_dir, "index.html")
    return send_file(entry)


api_bp = Blueprint("api_bp", __name__, url_prefix="/api")
rest_api = Api(api_bp)
app.register_blueprint(api_bp)

from api import *
