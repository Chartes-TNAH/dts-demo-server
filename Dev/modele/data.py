# Création du modèle selon celui de la base de données prosopochartes.sqlite

# Table correspondant à un.e chercheu.r.se
# Par souci de simplicité, chaque membre de la table est dans une relation many to one avec les autres tables
# (dans notre base, un.e chercheu.r.se n'a qu'un diplôme, une distinction...)
# Les relations sont donc identifiées par des clefs étrangères
class chants(db.Model):
    __tablename__ = "chants"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    Col = db.Column(db.TEXT)
    Collection_parent = db.Column(db.TEXT)
    Titre = db.Column(db.TEXT)
    Auteur = db.Column(db.TEXT)
    Interprete = db.Column(db.TEXT)
    Date_creation = db.Column(db.Integrer)
    Content = db.Column(db.TEXT)
    Link = db.Column(db.TEXT)


