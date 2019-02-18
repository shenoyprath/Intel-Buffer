import os

from peewee import MySQLDatabase

from utils.undef_env_var import error_if_undef


db_user_environ_var = "INTEL_BUFFER_DB_USER"
db_pass_environ_var = "INTEL_BUFFER_DB_PASS"

error_if_undef(db_user_environ_var)
error_if_undef(db_pass_environ_var)

db = MySQLDatabase(
    "intel_buffer_db",
    user=os.getenv(db_user_environ_var),
    password=os.getenv(db_pass_environ_var),
    charset="utf8mb4"
)
