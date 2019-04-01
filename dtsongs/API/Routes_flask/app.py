# j'importe du package flask les libraries Flask, render_template et Response, json, jsonify
from flask import Flask, render_template, Response, json, jsonify
# j'importe le package requests
import requests


# On instancie l'application DTSongs dans la variable app.
app = Flask('__DTSongs__')


# Création d'une classe de réponse pour l'application
class MyResponse(Response):
    # On déclare que xml devient le rendu par défaut de la route "/"
    default_mimetype = 'application/xml'
 
class chant_metadata(db.Model):
    chant_ID = db.Column(db.Integer, primary_key=True)
    Col = db.Column(db.String(45), unique=True, nullable=False)
    Collection_parent = db.Column(db.String(45), unique=True, nullable=False)
    Titre = db.Column(db.String(60), unique=True, nullable=False)
    Auteur = db.Column(db.String(45), nullable=False)
    Interp = db.Column(db.String(45))
    Date_creation = db.Column(db.Integer)
    Content = db.Column(db.String(120), unique=True, nullable=False)
    Link = db.Column(db.String(120), unique=True, nullable=False)


class chants_content(db.Model):
    PK_texte = db.Column(db.Integer, primary_key=True)
    Texte = db.Column(db.Text, nullable=False)
    id_line = db.Column(db.Integer)
    ordre_ligne = db.Column(db.Integer)
    fk_metadata = db.ForeignKey('chant_ID.id')

app.response_class = MyResponse


collection = {
     0: {
        "chant_id": "1",
        "Col": "Commune",
        "Collection_parent": "Collection_initiale",
        "Titre": "Le Temps des Cerises",
        "Auteur": "Jean-Baptiste Clément",
        "Interp": "Antoine Renard et alii",
        "Date_creation": "1868",
        "Content": "../../Collection_initiale/Commune/LeTempsdesCerises.txt",
        "Link": "https://fr.wikipedia.org/wiki/Le_Temps_des_cerises_(chanson)"},
     1: {"chant_id": "2",
         "Col": "1789_Révolution",
         "Collection_parent": "Collection_initiale",
         "Titre": "La Carmagnole",
         "Auteur": "anonyme",
         "Interp": "anonyme",
         "Date_creation": "1792",
         "Content": "../../Collection_initiale/1789_Révolution/Carmagnole.txt",
         "Link": "https://fr.wikipedia.org/wiki/La_Carmagnole"},
     2: {"chant_id": "3",
         "Col": "1789_Révolution",
         "Collection_parent": "Collection_initiale",
         "Titre": "La Marseillaise",
         "Auteur": "Rouget de l'Isle",
         "Interp": "Rouget de l'Isle",
         "Date_creation": "1792",
         "Content": "../../Collection_initiale/1789_Révolution/Marseillaise.txt",
         "Link": "https://fr.wikipedia.org/wiki/La_Marseillaise"},
     3: {"chant_id": "4",
         "Col": "Commune",
         "Collection_parent": "Collection_initiale",
         "Titre": "L'Internationale",
         "Auteur": "Eugnène Pottier",
         "Interp": "Gustave Nadaud",
         "Date_creation": "1871",
         "Content": "../../Collection_initiale/Commune/Internationale.txt",
         "Link": "https://fr.wikipedia.org/wiki/L%27Internationale"},
     4: {"chant_id": "5",
         "Col": "Chants_contre",
         "Collection_parent": "Collection_initiale",
         "Titre": "Le Triomphe de l'Anarchie",
         "Auteur": "Charles d'Avray",
         "Interp": "Charles d'Avray",
         "Date_creation": "1901",
         "Content": "../../Collection_initiale/Chants_contre/Triomphe_Anarchie.txt",
         "Link": "https://fr.wikipedia.org/wiki/Le_Triomphe_de_l%27anarchie"}
}

navigation = {
        "/Collection_initiale": member_of["1789_Révolution", "Commune", "Chants_contre"],
        "/Collection_initiale?id=1789_Révolution": member_of["Carmagnole.txt", "Marseillaise.txt"],
        "/Collection_intiale?id=Commune": member_of["Internationale.txt", "LeTempsdesCerises.txt"],
        "/Collection_initiale?id=Chants_contre": member_of["Triomphe_Anarchie.txt"],
        "/Collection_initiale?id=1789_Révolution/Carmagnole": member_of["Carmagnole.txt", "??"],
        "/Collection_initiale?id=1789_Révolution/Marseillaise": member_of["Marseillaise.txt", "??"],
        "/Collection_initiale?id=Commune/Internationale": member_of["Internationale.txt", "??"],
        "/Collection_initiale?id=Commune/LeTempsdesCerises": member_of["LeTempsdesCerises.txt", "??"],
        "/Collection_initiale?id=Chants_contre/Triomphe_Anarchie": member_of["Triomphe_Anarchie.txt", "??"]
    }

# print(json.dumps(collection))

# Collection-endpoit : il nous faut du Json en sortie :
# reste à définir les classes SQLAlchemy
# all_chants = chants_content.query.all()
# dict_chants = []
# for chant in all_chants:
    # dict_chants = {
        # 'fk_metadata': chants_content.fk_metadata,
        # 'column_name': table.column_values
    # }
    # print(json.dumps(dict_chants))


# grâce au décorateur app.route j'instancie la route de mon application Flask
# l'uilisation du "/" nous renseigne quant à l'endroit de la route, ici à la racine.
@app.route("/")
# je donne un nom au endpoint
def document_endpoint():
    """ route permettant de produire un document XML en sortie """
    return render_template("document.xml", nom="document_e")


# grâce au décorateur app.route j'instancie la route de mon application Flask
# l'utilisation du "/Collection" nous renseigne quant à l'endroit de la route, ici dans le niveau Collection
@app.route("/Collection")
# je donne un nom au endpoint
def collection_endpoint():
    """ route permettant la recherche dans la collection, output = json """
    requete = requests.args.get('chants.db', type=json)
    request = requete.query.filter_by(chants_id=chants_id).all()
# collection = []
    if request:
        #Si on fait print(json.dumps(collection)) dans ce cas on peut retourner du json dans le terminal.
        return jsonify(collection)


@app.route("/Navigation")
def navigation_endpoint():
    """ route permettant la navigation dans les collections, output = json """
    return jsonify(navigation)
