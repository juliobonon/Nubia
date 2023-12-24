from importlib import resources


def get_postgres_uri() -> str:
    with resources.path("src.database", "cepalhon.db") as sqlite_filepath:
        return f"sqlite:///{sqlite_filepath}"
