from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
import config

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    from app.models import db
    db.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)
    from app.resources import AuthorApi
    api.add_resource(AuthorApi, "/authors/<int:id>")

    return app

from app.models import Author, ToDo
