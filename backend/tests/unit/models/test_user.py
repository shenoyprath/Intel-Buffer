from string import printable

from hypothesis import given
from hypothesis.strategies import text, emails, characters

from models.user import User


from tests.unit.models.test_database_accessor import DatabaseAccessor


class TestUser(DatabaseAccessor):
    @staticmethod
    @given(first_name=text(characters(whitelist_categories=[], whitelist_characters=list(printable))),
           last_name=text(characters(whitelist_categories=[], whitelist_characters=list(printable))),
           email_address=emails(),
           password=text())
    def test_user_instantiation_inserts_user_to_db(first_name, last_name, email_address, password):
        test_user = User.instantiate(first_name, last_name, email_address, password)

        assert (User
                .select()
                .where(User.email_address == email_address)
                .count()) == 1

        test_user.delete_instance()
