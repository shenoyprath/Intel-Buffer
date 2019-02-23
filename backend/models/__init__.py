import os

from peewee import MySQLDatabase

from utils.undef_env_var import error_if_undef


db = MySQLDatabase(None)


def init_db(db_name):
    user_env_var = "INTEL_BUFFER_DB_USER"
    pass_env_var = "INTEL_BUFFER_DB_PASS"

    for env_var in (user_env_var, pass_env_var):
        error_if_undef(env_var)

    db.init(
        db_name,
        user=os.getenv(user_env_var),
        password=os.getenv(pass_env_var),
        charset="utf8mb4"
    )
    return db
