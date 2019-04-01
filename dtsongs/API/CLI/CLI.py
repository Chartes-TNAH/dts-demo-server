import click
import requests
import sqlite3

@click.command() 
def parse_DTSongs(q):
    """Parser la base de données chants contenant deux tables.
    :param q: Chaine de recherche
    :type q: str
    :return:

    """
    connexion = sqlite3.connect('chants.sqlite')
    cursor = connexion.cursor()

# req reste en gris chez moi, c'est normal ?
    req_ID = ('SELECT chant_ID FROM metadata_chants')
    req_col = ('SELECT Col FROM metadata_chants')
    req_col_parent = ('SELECT collection_parent FROM metadata_chants')
    req_titre = ('SELECT Titre FROM metadata_chants')
    req_auteur = ('SELECT Auteur FROM metadata_chants')
    req_interp = ('SELECT Interp FROM metadata_chants')

    click.echo(cursor)


@click.command()
# full=False reste en gris chez moi, c'est normal ?
def cherche_DTSongs(q, full=False):
    """ Chercher sur la base de données "chants" en faisant une requête

        :param q: Chaine de recherche
        :type q: str
        :param full: Recherche complète (itère sur toutes les tables)
        :type full: bool
        :returns: Tuple (
            Nombre de Résultats,
            Nombre de Pages,
            Liste de résultat sous forme de dictionnaire {uri, title, desc, author, date}
        )
        """
    # On exécute la requête dans la base de données.
    params = {"output": "json", "q": q, "page": page}
    req = requests.get("chants.sqlite", params=params)
    click.echo('chants.db')

    chant_ID, Col, Collection_parent, Titre, Auteur, Interp, Date_creation, \
    Content, Link = parser_DTSongs(req.json())

    return chant_ID, Col, Collection_parent, Titre, Auteur, Interp, Date_creation, Content, Link

