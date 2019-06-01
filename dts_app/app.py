from flask import Flask
# j'importe le package Flask de la librairie flask
from flask_sqlalchemy import SQLAlchemy
# j'importe SQLAlchemy de la librairie flask_sqlalchemy
from .config import CONFIG
# j'importe CONFIG de la librairie .config
# importer les packages des librairies et non les librairies complètes permet d'alléger le poids de l'application
# car dans ce cas on n'importe que les librairies dont on a besoin.
import os
# j'importe os

# deux chemins d'accès aux fichiers utilisés par l'application
chemin_actuel = os.path.dirname(os.path.abspath(__file__))
# la variable chemin_actuel contient le chemin absolu vers le fichier courant
templates = os.path.join(chemin_actuel, "templates")
# la variable templates contient le chemin d'accès aux dossiers templates depuis "chemin_actuel"


db = SQLAlchemy()
# db c'est l'instanciation de la database SQLAlchemy

app = Flask(
    # la variable app contient l'instanciation de l'application de type Flask
    __name__,
    # elle contient un nom "__name__"
    template_folder=templates
    # et le chemin d'accès au dossier des templates contenu dans la variable créée ci-dessus
)

# Import Scripts
from .script import db, create
# depuis le fichier script.py on importe les éléments db et create

# Import Routes
from .routes import collection_route, document_route, navigation_route, identifier_route
# elle apparaît comme inactive sur nos Pycharm, mais nous allons la commenter quand même
# depuis le fichier route on importe les fonctions collection_route, navigation_route, document_route et identifier_route


def config_app(config_name="test"):
    # création de la fonction de configuration de l'application, en paramètre le nom de l'application est "test"
    """ Create the application """
    app.config.from_object(CONFIG[config_name])
    # depuis app on appelle config et on appelle from_object qui contient les configurations.

    # Set up extensions
    db.init_app(app)
    # extensions de l'initialisation de la base de données dans app

    return app
# retourne l'application app