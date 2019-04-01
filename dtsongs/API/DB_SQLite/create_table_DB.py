# On importe les librairies dont on aura besoin: sqlite3 et csv.
import sqlite3, csv

# On instancie la connection à la base de données chants.bd avec la méthode
# .connect() et on stock cette création dans la variable connexion
connexion = sqlite3.connect('chants.db')

# On crée un curseur via la méthode .cursor()
# on stocke ce curseur dans la variable cursor
cursor = connexion.cursor()

# On autorise les clefs étrangères.
cursor.execute("PRAGMA foreign_keys = OFF")

# On exécute un scripte qui va créer les deux tables.
cursor.executescript('''CREATE TABLE IF NOT EXISTS chant_metadata 
(
chant_ID INTEGER PRIMARY KEY, 
Col TEXT, 
Collection_parent TEXT, 
Titre TEXT, 
Auteur TEXT,
Interp TEXT, 
Date_creation INTEGER, 
Content TEXT, 
Link TEXT
);
CREATE TABLE IF NOT EXISTS chants_content 
(
Texte TEXT NOT NULL,
id_line INTEGER PRIMARY KEY,
ordre_ligne INTEGER,
fk_metadata INTEGER NOT NULL,
FOREIGN KEY(fk_metadata) REFERENCES chant_metadata(chant_ID)
ON DELETE CASCADE);
DELETE FROM chant_metadata;
''')

# On sauvegarde les changements.
connexion.commit()

# On quitte la connexion.
connexion.close()
