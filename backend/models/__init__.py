from peewee import MySQLDatabase

from config import Config


db = MySQLDatabase(None)


def init_db(db_name):
    db.init(
        db_name,
        user=Config.DB_USER,
        password=Config.DB_PASS,
        charset="utf8mb4"
    )
    return db
