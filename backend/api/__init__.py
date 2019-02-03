import os

# noinspection PyUnresolvedReferences
from flask import Flask, Blueprint, current_app, send_file
from flask_restplus import Api

from peewee import MySQLDatabase

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.static_folder = os.path.join(app.config["DIST_DIR"], "static")


db_user_environ_var = "INTEL_BUFFER_DB_USER"
db_pass_environ_var = "INTEL_BUFFER_DB_PASS"
if os.environ.get(db_user_environ_var) is None:
    raise EnvironmentError(f"Environment variable {db_user_environ_var} isn't set to the username used to access the "
                           "database.")
if os.environ.get("INTEL_BUFFER_DB_PASS") is None:
    raise EnvironmentError(f"Environment variable {db_pass_environ_var} isn't set to the password used to access the "
                           "database.")

db = MySQLDatabase("intel_buffer_db",
                   user=os.environ.get("INTEL_BUFFER_DB_USER"),
                   password=os.environ.get("INTEL_BUFFER_DB_PASS"))


# noinspection PyUnusedLocal
@app.route("/", defaults={"path": ""})
@app.route("/<path>/")
def index(path):
    dist_dir = current_app.config["DIST_DIR"]
    entry = os.path.join(dist_dir, "index.html")
    return send_file(entry)


api_bp = Blueprint("api_bp", __name__, url_prefix="/api")
rest_api = Api(api_bp)
app.register_blueprint(api_bp)

from api import register
