import os


class UndefinedEnvironmentVariable(EnvironmentError):
    pass


def error_if_undef(env_var):
    if os.getenv(env_var) is None:
        raise UndefinedEnvironmentVariable(
            f"Environment variable '{env_var}' is undefined."
        )
