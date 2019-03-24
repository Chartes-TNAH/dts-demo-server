from app import db

class chants(db.Model):
    __tablename__ = "chanson"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    Col = db.Column(db.TEXT)
    Collection_parent = db.Column(db.TEXT)
    Titre = db.Column(db.TEXT)
    Auteur = db.Column(db.TEXT)
    Interprete = db.Column(db.TEXT)
    Date_creation = db.Column(db.TEXT)
    Content = db.Column(db.TEXT)
    Link = db.Column(db.TEXT)