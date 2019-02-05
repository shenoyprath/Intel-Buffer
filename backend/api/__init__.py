from flask import Blueprint

from flask_restplus import Api


api_blueprint = Blueprint("api", __name__, url_prefix="/api")
rest_api = Api(api_blueprint)

from api import login
