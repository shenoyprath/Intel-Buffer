from models.base import Base
from models.table_modifiers import create_tables, drop_tables


class TestTableModifiers:
    def test_drops_all_existing_tables(self, database):
        drop_tables()
        assert not database.get_tables()

    def test_create_tables_for_concrete_models(self, database):
        drop_tables()
        create_tables()
        # noinspection PyProtectedMember
        concrete_models = {model._meta.table_name for model in Base.get_concrete_descendants()}
        assert set(database.get_tables()) == concrete_models
