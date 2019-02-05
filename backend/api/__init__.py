from flask import Blueprint

from flask_restplus import Api


blueprint = Blueprint("api", __name__, url_prefix="/api")
rest_api = Api(blueprint)

from api import login
