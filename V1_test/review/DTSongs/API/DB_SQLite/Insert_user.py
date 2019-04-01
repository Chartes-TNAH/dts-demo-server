import sqlite3
# On instancie la connection à la base de données chants.bd avec la méthode
# .connect() et on stock cette création dans la variable connexion
connexion = sqlite3.connect('chants.db')

# On crée un curseur via la méthode .cursor()
# on stocke ce curseur dans la variable cursor
cursor = connexion.cursor()

print("Veuillez entrer les métadonnées pour la base chant_metadata:")
print("Entrez-les sous la forme: Col, Collection_parent, titre, auteur, interprète (s'il est connu), date (année), chemin vers le fichier, lien ")
line = input()

while True:
    if line == "":
        break

    cursor.execute('''INSERT INTO chant_metadata (chant_ID, Col, Collection_parent, Titre, Auteur, Interp, Date_creation, Content, Link)"
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", to_db)''', line).lastrowid


connexion.commit()

connexion.close()