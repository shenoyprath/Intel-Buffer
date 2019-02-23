import os


class UndefinedEnvironmentVariable(EnvironmentError):
    pass


def getenv_or_err(env_var):
    value = os.getenv(env_var)
    if value is None:
        raise UndefinedEnvironmentVariable(
            f"Environment variable '{env_var}' is undefined."
        )
    return value
