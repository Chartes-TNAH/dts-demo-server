import sqlite3
# On instancie la connection à la base de données chants.bd avec la méthode
# .connect() et on stock cette création dans la variable connexion
connexion = sqlite3.connect('chants.db')

# On crée un curseur via la méthode .cursor()
# on stocke ce curseur dans la variable cursor
cursor = connexion.cursor()


with open('..//..//Collection_initiale/1789_Révolution/Carmagnole.txt', 'r') as text:
    texte = text.read()

#cursor.execute("INSERT INTO chants_content('fk_metadata','TEXTE') VALUES (?, ?)", (SELECT chant_ID FROM chant_metadata WHERE Titre='Carmagnole', texte))
cursor.execute("INSERT INTO chants_content('fk_metadata','TEXTE') VALUES (?, ?)", (2 , texte))

with open('..//..//Collection_initiale/1789_Révolution/Marseillaise.txt', 'r') as text:
    texte = text.read()

cursor.execute("INSERT INTO chants_content('fk_metadata','TEXTE') VALUES (?, ?)", (3 , texte))

with open('..//..//Collection_initiale/Chants_contre/Triomphe_Anarchie.txt', 'r') as text:
    texte = text.read()

cursor.execute("INSERT INTO chants_content('fk_metadata','TEXTE') VALUES (?, ?)", (5 , texte))

with open('..//..//Collection_initiale/Commune/Internationale.txt', 'r') as text:
    texte = text.read()

cursor.execute("INSERT INTO chants_content('fk_metadata','TEXTE') VALUES (?, ?)", (4 , texte))

with open('..//..//Collection_initiale/Commune/LeTempsdesCerises.txt', 'r') as text:
    texte = text.read()

cursor.execute("INSERT INTO chants_content('fk_metadata','TEXTE') VALUES (?, ?)", (1 , texte))

connexion.commit()

connexion.close()