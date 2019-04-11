import os
import csv

import click

from .app import app, db
from .models import Triple, Collection, Passage


@app.cli.group("db")
def db_cli():
    """ """
    pass


@db_cli.command()
def create():
    db.create_all()


@db_cli.command()
@click.argument("tsv", type=click.File(mode="r"))
def load(tsv: click.File):
    db.drop_all()
    db.create_all()

    directory = os.path.abspath(os.path.dirname(tsv.name))
    reader = csv.reader(tsv, delimiter="\t")
    columns = None

    collections = {}
    mandatories = ["@id", "@parent", "@title", "@content"]

    for line in reader:
        if not columns:
            columns = tuple(line)
            missing = [
                column
                for column in mandatories
                if column not in columns
            ]
            if len(missing):
                print("Your TSV file is missing the following columns : " + ", ".join(missing))
                return None
        else:
            main_keys = dict(zip(columns, line))

            collection_type = "Collection"
            if main_keys["@content"]:
                collection_type = "Resource"

            collection = Collection(
                collection_identifier=main_keys["@id"],
                collection_parent=collections.get(main_keys["@parent"], None),
                collection_title=main_keys["@title"],
                collection_type=collection_type
            )
            db.session.add(collection)
            db.session.flush()
            collections[main_keys["@id"]] = collection.collection_id

            for predicate, value in zip(columns, line):
                if value and predicate not in mandatories:
                    triple = Triple(
                        triple_subject=collection.collection_id,
                        triple_predicate=predicate,
                        triple_object=value
                    )
                    db.session.add(triple)

            if main_keys["@content"]:
                with open(os.path.join(directory, main_keys["@content"])) as f:
                    identifier = 1
                    for raw_line in f.readlines():
                        line = raw_line.strip()
                        if line:
                            passage = Passage(
                                passage_order=identifier,
                                passage_value=line,
                                passage_collection=collection.collection_id
                            )
                            identifier += 1
                            db.session.add(passage)
        db.session.commit()
