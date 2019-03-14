# On importe les packages csv et sqlite3
import csv
import sqlite3

# On se connecte à la base chants via la méthode .connect.
# On stock la connection dans la variable connection.
connection = sqlite3.connect('chants.db')

# On crée un curseur via la méthode .cursor()
# on stock ce curseur dans la variable cursor.
cursor = connection.cursor()

# On ouvre en mode lecture notre fichier TSV et on le stock dans la variable file.
with open('..//Python/chansons.tsv', 'r') as file:
	# Dans la variable dico, on stock le dictionnaire extrait à partir
	# de notre variable file en lui passant en paramètre le délimiteur \t.
	dico = csv.DictReader(file, delimiter='\t')
	# dans la variable to_db, on stock la boucle for qui parse le dictionnaire dico
	# et qui stocke les valeurs des différentes clefs. 
	to_db = [(i['ID'], i['collection'], i['collection_parent'], i['Titre'], i['Auteur'],
	 i['Interprete'], i['Date'],i['Content'], i['Link'] ) for i in dico]

# On insère, via la méthode .execute, les valeurs présente dnas dico dans la table chanson.
cursor.executemany("INSERT INTO chanson (ID, Col, Collection_parent, Titre, Auteur, Interprete, Date_creation, Content, Link) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", to_db)

# On sauvegarde les changements avec la méthode .commit.
connection.commit()

# On se déconnecte de la base de données avec .close.
connection.close()