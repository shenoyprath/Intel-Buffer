import os
import sys

from flask import Flask
from flask_jwt_extended import JWTManager

from logger import logger
from config import Config

from index import index

from api import api_blueprint

from models import db
from models.base import Base


if sys.version_info < (3, 7):
    raise RuntimeError("Python version >= 3.7 is required.")


app = Flask(__name__)
app.config.from_object(Config)
app.static_folder = os.path.join(app.config["DIST_DIR"], "static")

app.add_url_rule(rule="/", view_func=index, defaults={"path": ""})
app.add_url_rule(rule="/<path>/", view_func=index)

app.register_blueprint(api_blueprint)

JWTManager(app)

with db:
    db.create_tables(Base.__subclasses__(), safe=True)


if __name__ == "__main__":
    logger()
    app.run(host="0.0.0.0", port=8888, debug=True)
