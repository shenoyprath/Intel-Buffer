from models.base import Base


def create_tables():
    for descendant in Base.get_concrete_descendants():
        descendant.create_table()


def drop_tables():
    for descendant in Base.get_concrete_descendants():
        if descendant.table_exists():
            descendant.drop_table()
