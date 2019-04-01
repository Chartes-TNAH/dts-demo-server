# On importe les librairies dont on aura besoin: sqlite3 et csv.
import sqlite3, csv

# On instancie la connection à la base de données chants.bd avec la méthode
# .connect() et on stock cette création dans la variable connexion
connexion = sqlite3.connect('chants.db')

# On crée un curseur via la méthode .cursor()
# on stocke ce curseur dans la variable cursor
cursor = connexion.cursor()

with open('..//Metadata/Chansons.tsv', 'r') as file:
	# Dans la variable dico, on stock le dictionnaire extrait à partir
	# de notre variable file en lui passant en paramètre le délimiteur \t.
	dico = csv.DictReader(file, delimiter='\t')
	# dans la variable to_db, on stock la boucle for qui parse le dictionnaire dico.
	to_db = [(i['ID'], i['collection'], i['collection_parent'], i['Titre'], i['Auteur'],
	 i['Interprete'], i['Date'],i['Content'], i['Link'] ) for i in dico]


# On insère, via la méthode .execute, les valeurs présente dnas dico dans la table chanson.
cursor.executemany("INSERT INTO chant_metadata (chant_ID,"
                   "Col,"
                   "Collection_parent,"
                   "Titre,"
                   "Auteur,"
                   "Interp,"
                   "Date_creation,"
                   "Content,"
                   "Link)"
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", to_db)


#cursor.execute("INSERT INTO chants_content('fk_metadata','TEXTE') VALUES (?, ?)", (SELECT chant_ID FROM chant_metadata WHERE Titre='Carmagnole', texte))

connexion.commit()

#for chant in cursor.execute("SELECT * FROM chant_metadata"):
    #print("chant_meta :", chant)

#for content in cursor.execute("SELECT * FROM chant_content"):
    #print("chant_cont :", content)

connexion.close()