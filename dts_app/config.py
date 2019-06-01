class _TEST:
    # On créé la classe TEST qui permet de configurer la db en version TEST
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite'
    # On configure la base de données et l'adresse qui y est lié
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # On renvoie FALSE à la liste de toutes les modifications


class _DEV:
    # On créé la classe DEV qui permet de configurer la db en version DEV
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.sqlite'
    # On configure la base de données et l'adresse qui y est lié
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # On renvoie FALSE à la liste de toutes les modifications :
    # ce qui permet de ne pas alourdir le code et de ne pas renvoyer d'erreur


CONFIG = {
    # dictionnaire qui contient les deux classes et qu'on pourra appelé dans les autres fichiers
    "test": _TEST,
    "dev": _DEV
}