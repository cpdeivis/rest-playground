class Config(object):
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'lorem-ipsum'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:////home/cpdeivis/playground/rest-playground/database.db"
    EXTENSIONS = [
        "playground.ext.database:init_app",
        "playground.ext.migrate:init_app",
        "playground.blueprints.api:init_app"
    ]

