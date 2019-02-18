from hypothesis import given
from hypothesis.strategies import text

from pytest import raises

from utils.undef_env_var import error_if_undef, UndefinedEnvironmentVariable


class TestUndefEnvVar:
    @given(env_var=text())
    def test_errors_undef_env_var(self, env_var):
        with raises(UndefinedEnvironmentVariable):
            error_if_undef(env_var)
