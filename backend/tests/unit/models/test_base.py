from pytest import mark

from hypothesis import given
from hypothesis.strategies import integers

from models.base import Base
from models.user import User


class TestBase:
    @mark.usefixtures("database")
    @given(id_=integers())
    def test_safe_get_by_id_returns_none_when_not_found(self, id_):
        assert User.safe_get_by_id(id_) is None

    def test_get_concrete_descendants(self):
        """
        Class hierarchy/tree for testing this method:
                                            AbstractModel1
                                            |            |
                                    AbstractModel2    ConcreteModel1
                                            |            |
                                    ConcreteModel3    ConcreteModel2
                                            |
                                    AbstractModel3
                                            |
                                    ConcreteModel4
        """

        # noinspection PyAbstractClass
        class AbstractModel1(Base):
            __is_abstract = True

        # noinspection PyAbstractClass
        class AbstractModel2(AbstractModel1):
            __is_abstract = True

        # noinspection PyAbstractClass
        class ConcreteModel1(AbstractModel1):
            pass

        # noinspection PyAbstractClass
        class ConcreteModel2(ConcreteModel1):
            pass

        # noinspection PyAbstractClass
        class ConcreteModel3(AbstractModel2):
            pass

        # noinspection PyAbstractClass
        class AbstractModel3(ConcreteModel3):
            __is_abstract = True

        # noinspection PyAbstractClass
        class ConcreteModel4(AbstractModel3):
            pass

        # concrete descendants of AbstractModel1
        expected = {ConcreteModel1, ConcreteModel2, ConcreteModel3, ConcreteModel4}
        actual = {model for model in AbstractModel1.get_concrete_descendants()}
        assert actual == expected
