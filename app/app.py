# On importe le module Flask de la librairie Flask
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

# On importe le module os pour gérer les chemins de fichiers
import os

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")

# On définit ici le nom de l'application, le lieu où se trouve les templates.
app = Flask("DTSOngs",
            template_folder=templates,
            )

# On créé le lien avec la base de données sqlite chants.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB/chants.sqlite'
# Permet d'afficher les commandes de requêtes de SQLAlchemy.
app.config['SQLALCHEMY_ECHO'] = True
# Instanciation du mode debug, cette fonction est liée au fichier .flaskenv
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['DEBUG'] = True

# Intégration de l'extension SQLAlchemy à notre application Flask ;
# nous stockons notre base de données dans la variable db
db = SQLAlchemy(app)

class Rep():
    default_mimetype = 'application/xml'

class JSON_Rep():
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(JSON_Rep, cls).force_type(rv, environ)

@app.route('/données.xml')
def get_donnees():
    id = query.get(ID)
    return render_template('données.xml', id = ID)

@app.route('/données.xml')
def get_donnees_json():
    return render_template(jsonify('données.xml'))