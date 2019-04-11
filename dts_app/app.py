from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import CONFIG
import os

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")


db = SQLAlchemy()

app = Flask(
    __name__,
    template_folder=templates
)

# Import Scripts
from .script import db, create

# Import Routes
from .routes import collection_route, document_route, navigation_route, identifier_route


def config_app(config_name="test"):
    """ Create the application """
    app.config.from_object(CONFIG[config_name])

    # Set up extensions
    db.init_app(app)

    return app

