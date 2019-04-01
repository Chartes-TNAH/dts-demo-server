# On importe deux librairies: csv et sqlite3.
import csv
import sqlite3

# On instancie la connection à la base de données chants.bd avec la méthode
# .connect et on stocke cette création dans la variable connection.
connection = sqlite3.connect('chants.db')

# On créé un curseur via la méthode .cursor()
# on stocke ce curseur dans la variable cursor.
cursor = connection.cursor()

# On utilise la variable cursor auquel on colle la méthode .execute
# cela permet d'exécuter une commande dans la base SQL.
# Ici, on créé une table chanson.
# On spécifie le type des entrées colonnes présente dans la table chanson.
cursor.execute('''CREATE TABLE chanson (ID integer, 
	Col TEXT, 
	Collection_parent TEXT, 
	Titre TEXT, 
	Auteur TEXT, 
	Interprete TEXT, 
	Date_creation integer, 
	Content TEXT, 
	Link TEXT);''')

# Pour sauvegarder les changements dans la base,
# on utilise la méthode .commit.
connection.commit()

#La méthode .close permet quand à elle de stopper la connexion
#à la base de données. 
connection.close()
