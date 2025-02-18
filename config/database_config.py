from . import env


class DatabaseConfig:
    """
        Database configuration data.
    """
    DB_USER = env.str("DATABASE_USER")
    DB_PASSWORD = env.str("DATABASE_PASSWORD")
    DB_NAME = env.str("DATABASE")
    DB_HOST = env.str("DATABASE_HOST")
    DB_PORT = env.str("DATABASE_PORT")