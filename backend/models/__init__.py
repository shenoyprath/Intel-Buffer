from peewee import MySQLDatabase


db = MySQLDatabase(None)


def init_db(config):
    db.init(
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASS,
        charset="utf8mb4"
    )
    return db
