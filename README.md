DTS-Demo-Server
===============

# Run

- `FLASK_DEBUG=True flask run` to run the API


# Navigation example

Load example by running `flask db load example_data.tsv` you can then navigate to 
collection/endpoint
navigation/endpoint
and
document/endpoint


This server supports all parameters from http://w3id.org/dts except the pagination ones. 
1. http://127.0.0.1:5000/
2. http://127.0.0.1:5000/collection?id=/chants_contre
3. [http://127.0.0.1:5000/collection?id=https://www.wikidata.org/wiki/Q3227832](http://127.0.0.1:5000/collection?id=https://www.wikidata.org/wiki/Q3227832)
4. [http://127.0.0.1:5000/navigation?id=https://www.wikidata.org/wiki/Q3227832](http://127.0.0.1:5000/navigation?id=https://www.wikidata.org/wiki/Q3227832)
5. [http://127.0.0.1:5000/document?id=https://www.wikidata.org/wiki/Q3227832&start=1&end=10](http://127.0.0.1:5000/document?id=https://www.wikidata.org/wiki/Q3227832&start=1&end=10)

# Older Readme


Présentation du projet :

"DTS-Demo-Server" est une API issue (comme son nom l'indique) de DTS, qui vise 
à rendre accessible et interrogeable une base de données composée de chants.
Ce projet est développé avec Python3 dans le cadre du Master 2 TNAH de l'Ecole des Chartes.



Pour l'installation en local des librairies correspondantes, il vous sera nécessaire de taper la commande suivante dans votre terminal :
pip install -r requirements.txt

Pour utiliser le projet vous aurez besoin de :
1. Installer python3
2. Dédier un environnement virtuel au projet
3. Cloner / Forker & Cloner le repository
4. Installer les librairies indiquées dans le fichier requirements.txt
5. Dans le dossier dtsongs qui contient l'application lancer la commande flask run.
