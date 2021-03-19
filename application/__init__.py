from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from application.config import Config
from pyutils.http.schema_validation import SchemaValidation
from pyutils.auth.flaskjwt import FlaskJWT


class Application:
    app = None
    db = None
    migration = None
    schema = None
    auth = None


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    if Config.SQLALCHEMY_DATABASE_URI:
        Application.db = SQLAlchemy(
            app, session_options={"expire_on_commit": False})
        Application.migration = Migrate(app, Application.db)
    Application.app = app
    Application.schema = SchemaValidation("application/spec/swagger-flat.yml")
    if Config.RSA_PUBLIC_KEY:
        Application.auth = FlaskJWT(Config.RSA_PUBLIC_KEY, ["RS256"])

    import application.views

    return app
