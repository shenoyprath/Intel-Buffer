import os
from string import ascii_letters, digits

from hypothesis import given
from hypothesis.strategies import text, characters

from pytest import raises, fail

from utils.undef_env_var import error_if_undef, UndefinedEnvironmentVariable


class TestUndefEnvVar:
    @given(env_var=text())
    def test_errors_undef_env_var(self, env_var):
        with raises(UndefinedEnvironmentVariable):
            error_if_undef(env_var)

    @given(env_var=text(
        characters(
            whitelist_characters=tuple(ascii_letters + digits),  # avoids encoding & illegal name errors
            whitelist_categories=()
        ),
        min_size=1
    ))
    def test_passes_defined_env_var(self, env_var):
        os.environ[env_var] = env_var
        try:
            error_if_undef(env_var)
        except UndefinedEnvironmentVariable:
            fail(
                f"Raised UndefinedEnvironmentVariable exception when "
                f"environment variable '{env_var}' was defined."
            )
        finally:
            del os.environ[env_var]
