import os
# on importe la librairie os
import csv
# on importe la librairie csv

import click
# on importe la librarie click

from .app import app, db
# on importe app et db depuis le fichier app.py
from .models import Triple, Collection, Passage
# on importe Triple, Collection, Passage depuis le fichier models.py


@app.cli.group("db")
# on crée un cli à partir de la database
def db_cli():
    # et on lance cli avec def db_cli():
    """ """
    pass


@db_cli.command()
# création de la ligne de commande qui permet de lancer la db
def create():
    # on crée la database une fois
    db.create_all()
    # ligne de code qui crée la databse dans la fonction create


@db_cli.command()
# ligne de commande qui permet de lancer la db
@click.argument("tsv", type=click.File(mode="r"))
# on passe en paramètres (argument dans cli) un tsv, de type fichier qui soit en mode lecture
def load(tsv: click.File):
    # définition de la fonction load qui permet de charger ce fichier
    db.drop_all()
    # on supprime la db avec drop_all
    db.create_all()
    # on recrée une db vide

    directory = os.path.abspath(os.path.dirname(tsv.name))
    # variable qui récupère le chemin(absolu) vers le fichier tsv
    reader = csv.reader(tsv, delimiter="\t")
    # variable reader qui contient la méthode reader du tsv et on donne comme délimitation \t
    columns = None
    # on déclare qu'il n'y a pas de colonne dans cette nouvelle db

    collections = {}
    # on crée un dictionnaire collection vide
    mandatories = ["@id", "@parent", "@title", "@content"]
    # on met dans une variable madatories le nom des colonnes (id, parent, title, content)

    for line in reader:
        # pour chaque ligne dans reader
        if not columns:
            # s'il n'y a pas de colonne
            columns = tuple(line)
            # on récupéère les colonnes dans le tuple de la première ligne
            missing = [
                # variable missing dans laquelle on fait une liste des noms de colonnes
                column
                for column in mandatories
                # si les colonnes sont bien présentes dans la variable mandatories on les récupére
                if column not in columns
                   # sinon
            ]
            if len(missing):
                # s'il manque une colonne
                print("Your TSV file is missing the following columns : " + ", ".join(missing))
                # on renvoie un message qui print "Your TSV file is missing the following columns :" + ",".join(missing)
                return None
            # ne retourne pas d'objet, pas de fichier
        else:
            # si cette fois-ci on a déjà des colonnes alors :
            main_keys = dict(zip(columns, line))
            # on crée la variable main_keys qui contient un dictionnaire du zip
            # de l'ensemble des colonnes et des lignes et qui permet de passer sur un itérable
            collection_type = "Collection"
            # on définit que le collection_type est Collection
            if main_keys["@content"]:
                # mais si dans le main_keys on a la colonne content
                collection_type = "Resource"
                # alors le collection_type est Resource

            collection = Collection(
                # dans la variable collection on crée un objet Collection qui contient les noms des colonnes
                # qu'on a défini dans models.py
                collection_identifier=main_keys["@id"],
                # un collection_identifier (@id)
                collection_parent=collections.get(main_keys["@parent"], None),
                # un collection_parent (@parent)
                collection_title=main_keys["@title"],
                # un collection_title (@title)
                collection_type=collection_type
                # un collection_type (@collection_type)
            )
            db.session.add(collection)
            # on ajoute cette collection à la db
            db.session.flush()
            # grâce au buffer flush on évacue les informations précédentes et on recommence
            collections[main_keys["@id"]] = collection.collection_id
            # dans le dictionnaire collections pour l'entrée main_keys qui se nomme @id
            # elle est égale à l'id de la collection

            for predicate, value in zip(columns, line):
                # pour predicate et value dans zip qui contient les colonnes et les lignes
                if value and predicate not in mandatories:
                    # si value et predicate ne sont pas dans mandatories
                    triple = Triple(
                        # on stocke la classe Triple dans une variable triple qui va servir à construire le triplet
                        triple_subject=collection.collection_id,
                        # l'id de la collection renvoie au sujet
                        triple_predicate=predicate,
                        # le predicat renvoie au predicat
                        triple_object=value
                        # la valeur renvoie à l'objet
                    )
                    db.session.add(triple)
                    # on ajoute la variable triple à notre db

            if main_keys["@content"]:
                # on récupère la valeur de content dans main_keys
                with open(os.path.join(directory, main_keys["@content"])) as f:
                    # on cherche le chemin du fichier contenu dans le répertoire qui y est lié en tant que variable f
                    identifier = 1
                    # on défini l'identifier comme portant le numéro 1
                    for raw_line in f.readlines():
                        # pour chaque raw_line dans f on la lit grâce à la méthode readlines
                        line = raw_line.strip()
                        # dans la variable ligne on stocke la ligne récupérée moins
                        # les espaces inutiles de début et de fin
                        if line:
                            # si il y a une ligne
                            passage = Passage(
                                # on stocke Passage dans la variable passage
                                passage_order=identifier,
                                # l'identifiant est stocké dans passage_order
                                passage_value=line,
                                # la ligne dans passage_value
                                passage_collection=collection.collection_id
                                # et l'id dans passage_collection
                            )
                            identifier += 1
                            # on incrémente identifier
                            db.session.add(passage)
                            # et on l'add sur notre db
        db.session.commit()
        # on fait un commit pour enregistrer les modifications
