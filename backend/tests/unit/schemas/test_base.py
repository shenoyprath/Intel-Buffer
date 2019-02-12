from schemas.base import Base


class TestBase:
    @staticmethod
    def test_strict_enabled():
        assert Base.Meta.strict
