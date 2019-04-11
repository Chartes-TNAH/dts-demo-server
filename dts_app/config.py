class _TEST:
    # On configure la base de données
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class _DEV:
    # On configure la base de données
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


CONFIG = {
    "test": _TEST,
    "dev": _DEV
}