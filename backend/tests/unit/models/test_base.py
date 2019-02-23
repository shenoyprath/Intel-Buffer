from pytest import mark

from hypothesis import given
from hypothesis.strategies import integers

from models.user import User


@mark.usefixtures("database")
class TestBase:
    @given(id_=integers())
    def test_safe_get_by_id_returns_none_when_not_found(self, id_):
        assert User.safe_get_by_id(id_) is None
