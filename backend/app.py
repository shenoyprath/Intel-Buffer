import os
import sys

from flask import Flask

from config import Config
from index import index
from logger import logger

from api import api_blueprint, jwt

from models import db
from models.base import Base


if sys.version_info < (3, 7):  # pragma: no cover
    raise RuntimeError("Python version >= 3.7 is required.")


def create_app():
    new_app = Flask(__name__)
    new_app.config.from_object(Config)
    new_app.static_folder = os.path.join(
        new_app.config["DIST_DIR"],
        "static"
    )

    new_app.add_url_rule(
        rule="/",
        view_func=index,
        defaults={"path": ""}
    )
    new_app.add_url_rule(
        rule="/<path>",
        view_func=index
    )

    def register_blueprints():
        new_app.register_blueprint(api_blueprint)

    def register_extensions():
        jwt.init_app(new_app)

    register_blueprints()
    register_extensions()

    return new_app


app = create_app()

with db:
    db.create_tables(Base.__subclasses__(), safe=True)


if __name__ == "__main__":
    logger()
    app.run(host="0.0.0.0", port=8888, debug=True)
