import os

from peewee import MySQLDatabase


db_user_environ_var = "INTEL_BUFFER_DB_USER"
db_pass_environ_var = "INTEL_BUFFER_DB_PASS"

if os.environ.get(db_user_environ_var) is None:
    raise EnvironmentError(f"Environment variable {db_user_environ_var} isn't set to the username used to access "
                           f"the database.")
if os.environ.get(db_pass_environ_var) is None:
    raise EnvironmentError(f"Environment variable {db_pass_environ_var} isn't set to the password used to access "
                           f"the database.")

db = MySQLDatabase("intel_buffer_db",
                   user=os.environ.get("INTEL_BUFFER_DB_USER"),
                   password=os.environ.get("INTEL_BUFFER_DB_PASS"))
