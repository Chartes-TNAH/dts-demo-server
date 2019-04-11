from .app import db


class Triple(db.Model):
    __tablename__ = "triple"
    triple_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    triple_subject = db.Column(db.Text, db.ForeignKey('collection.collection_id'), nullable=False)
    triple_predicate = db.Column(db.Text, nullable=False)
    triple_object = db.Column(db.Text, nullable=False)


class Collection(db.Model):
    __tablename__ = "collection"
    collection_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    collection_identifier = db.Column(db.Text, unique=True, nullable=False)
    collection_parent = db.Column(db.Text, db.ForeignKey('collection.collection_id'))
    collection_title = db.Column(db.Text, nullable=False)
    collection_type = db.Column(db.Text, default="Collection")

    triples = db.relationship("Triple")
    passages = db.relationship("Passage", order_by="Passage.passage_order")

    @property
    def authors(self):
        return Triple.query.filter(db.and_(
            Triple.triple_subject == self.collection_id,
            Triple.triple_predicate == "http://purl.org/dc/elements/1.1/creator"
        )).all()

    @staticmethod
    def get_by_identifier(identifier):
        return Collection.query.filter(Collection.collection_identifier == identifier).first()


class Passage(db.Model):
    __tablename__ = "passage"
    passage_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    passage_collection = db.Column(db.Text, db.ForeignKey('collection.collection_id'), nullable=False)
    passage_order = db.Column(db.Integer, nullable=False)
    passage_value = db.Column(db.Text)
    passage_tag = db.Column(db.Text, default="l")
