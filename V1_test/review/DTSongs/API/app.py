# On importe le module Flask de la librairie flask.
from flask import Flask

# On instancie l'application DTSongs dans la variable app.
app = Flask(__DTSongs__)

# Création d'une classe de réponse pour l'application
class MyResponse(Response):
    # On déclare que xml devient le rendu par défaut de l'API
    default_mimetype = 'application/xml'

app = Flask(__name__)
app.response_class = MyResponse

@app.route('/')
def bienvenu():
    return 'Bienvenu sur DTSongs'

@app.route('/xml')
    return render_template('/file_xml.xml')