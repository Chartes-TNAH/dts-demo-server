from sqlalchemy import func
# on importe func de la librairie sqlalchemy
from sqlalchemy.ext.hybrid import hybrid_property
# on importe hybrid_property depuis l'extension hybrid de la librairie sqlalchemy
from .app import db
# on importe db de app.py
import os
import csv


class Triple(db.Model):
    # Création de la classe Triple, d'une table triple
    # contenant un id, un subject, un prédicat et un objet en colonne
    # modèle de classe du triplet rdf
    __tablename__ = "triple"
    triple_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    # On donne des paramètres aux colonnes, le type de donnée, le caractère unique etc.
    triple_subject = db.Column(db.Text, db.ForeignKey('collection.collection_id'), nullable=False)
    # On fait appelle à une clef étrangère présente dans une autre table.
    triple_predicate = db.Column(db.Text, nullable=False)
    triple_object = db.Column(db.Text, nullable=False)

# les définitions de classe en python étant récurentes nous n'avons commenté que la première
class Collection(db.Model):
    __tablename__ = "collection"
    collection_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    collection_identifier = db.Column(db.Text, unique=True, nullable=False)
    collection_parent = db.Column(db.Text, db.ForeignKey('collection.collection_id'))
    collection_title = db.Column(db.Text, nullable=False)
    collection_type = db.Column(db.Text, default="Collection")

    triples = db.relationship("Triple")
    # on crée une relation one to many entre les tables "Triple", "Passage", et "Collection"
    passages = db.relationship("Passage", order_by="Passage.passage_order")
    # https://stackoverflow.com/questions/34775701/one-to-many-relationship-on-same-table-in-sqlalchemy
    children = db.relationship("Collection", backref=db.backref('parent', remote_side=[collection_id]))

    @hybrid_property
    # propriétés qui permettent sur des classes de compter le nombre d'items
    def total_items(self):
        # fonction qui prend comme paramètre elle-même
        return len(self.children)
    # grâce à la méthode len() on retourne le nb d'items contenus dans la classe

    @total_items.expression
    # permet de compter tous les items requêtés et de les filtrer
    def _total_item_expression(cls):
        # fonction qui prend en paramètre cls (=classe)
        return db.session.query(func.count(Collection.collection_id)).filter(
            Collection.collection_parent == cls.collection_id
        ).scalar()
    # et retourne une requête sur la db qui est une fonction qui compte le nb d'id
    # dans collection et qui les filtre en fonction de la collection parent à laquelle ils appartiennent
    # la méthode scalar() permet de les afficher à la suite

    @property
    # décorateur qui permet de définir des propriétés sur l'ensemble des modèles
    def authors(self):
        # On retourne une requête sur la classe Triple qui filtre à la fois l'élément triple_subject
        # et triple_predicate. On vérifie que le sujet correspond à l'id de la classe collection et que
        # le prédicat est présent dans dc terms creator. On récupère tous les résultats.
        return Triple.query.filter(db.and_(
            Triple.triple_subject == self.collection_id,
            Triple.triple_predicate == "http://purl.org/dc/terms/creator"
        )).all()


    @staticmethod
    # décorateur qui créé un méthode statique.
    def get_by_identifier(identifier):
        # Fonction qui récupère les éléments de la classe collection en fonction de leur identifier
        # on ne récupère que le premier grâce à la méthode .first()
        return Collection.query.filter(Collection.collection_identifier == identifier).first()


class Passage(db.Model):
    __tablename__ = "passage"
    passage_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    passage_collection = db.Column(db.Text, db.ForeignKey('collection.collection_id'), nullable=False)
    passage_order = db.Column(db.Integer, nullable=False)
    passage_value = db.Column(db.Text)
    passage_tag = db.Column(db.Text, default="l")
