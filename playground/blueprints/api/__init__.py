from flask import Blueprint
from flask_restful import Api

from .resources import AuthorApi, AuthorListApi


bp = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(bp)


def init_app(app):
    api.add_resource(AuthorApi, "/authors/<int:id>")
    api.add_resource(AuthorListApi, '/authors')
    app.register_blueprint(bp)
