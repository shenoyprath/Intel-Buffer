import os
import sys

from flask import Flask

from config import DevConfig
from index import index
from logger import logger

from api import api_blueprint, jwt

from models import init_db
from models.table_modifiers import create_tables


if sys.version_info < (3, 7):  # pragma: no cover
    raise RuntimeError("Python version >= 3.7 is required.")


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.static_folder = os.path.join(
        app.config["DIST_DIR"],
        "static"
    )

    app.add_url_rule(
        rule="/",
        view_func=index,
        defaults={"path": ""}
    )
    app.add_url_rule(
        rule="/<path>",
        view_func=index
    )

    def register_blueprints():
        app.register_blueprint(api_blueprint)

    def register_extensions():
        jwt.init_app(app)

    register_blueprints()
    register_extensions()

    return app


if __name__ == "__main__":
    application = create_app(DevConfig)
    init_db(DevConfig)
    create_tables()

    logger()
    application.run(host="0.0.0.0", port=8888, debug=True)
