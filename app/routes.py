from flask import render_template, jsonify

# Cette commande permet d'importer, depuis notre package app, la variable app qui instancie notre application.
from app import app

@app.route('/données.xml')
def get_donnees():
    return render_template('données.xml', name=name)


@app.route('/données_json.json')
def get_donnees_json():
    return jsonify(get_donnees)

