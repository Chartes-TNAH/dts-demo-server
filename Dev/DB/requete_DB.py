# Importation du module sqlite3
import sqlite3

# Connexion à la base de données chants.db avec la méthode .connect()
conn = sqlite3.connect('chants.db')
# Instanciation d'un curseur avec .cursor et stockage
# du curseur dans la variable c.
c = conn.cursor()

# L'objet buffer en python permet de stocker temporairement des données
# et de les présenter dans un format brut.
buffer = ""

# On affiche deux messages pour les utilisateurs.
# Le premier message indique aux utilisateurs
# qu'ils doivent rédiger leur requête au format de requête SQL, à savoir le Query.
print("Entrez votre requête SQL à exécuter en sqlite3.")
# On indique ici ce qui permet à l'utilisateur de sortir de la zone de saisie Query.
print("Entrez une ligne vide pour sortir du code.")

# Tant que While vaut True, la ligne contient input utilisateur.
# Si la ligne est constituée uniquement d'un blanc, le code s'arrête.
while True:
    line = input()
    if line == "":
        break

    # Le buffer contient l'input de l'utilisteur stocké dans line.
    buffer += line

    # Si le contenu de buffer correspond à une requête bien formée SQL,
    if sqlite3.complete_statement(buffer):
        # on nettoie la chaine de caractères présentes dans buffer.
        try:
            buffer = buffer.strip()
            # on exécute le buffer.
            c.execute(buffer)
            # Si le premier mot du buffer correspond à SELECT
            if buffer.lstrip().upper().startswith("SELECT"):
                #on va chercher toutes les réponses et on les print à l'écran.
                print(c.fetchall())
        # en cas d'erreur dans les étapes précédentes, on stocke les erreurs dans une variable e
        except sqlite3.Error as e:
            # on affiche à l'utilisateur un message d'erreur et le code de l'erreur.
            print("Une erreur est survenue:", e.args[0])
        # en dernier, on vide le buffer.
        buffer = ""
# On n'oublie pas de refermer la connexion à la base de données.
conn.close()


