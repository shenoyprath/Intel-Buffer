from string import printable

from werkzeug.security import check_password_hash

from hypothesis import given
from hypothesis.strategies import text, emails, characters

from models.user import User

from utils.remove_extra_spaces import remove_extra_spaces

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

    @staticmethod
    @given(first_name=text(characters(whitelist_categories=[], whitelist_characters=list(printable))),
           last_name=text(characters(whitelist_categories=[], whitelist_characters=list(printable))),
           email_address=emails(),
           password=text())
    def test_user_instantiation_removes_extra_spaces_in_names(first_name, last_name, email_address, password):
        test_user = User.instantiate(first_name, last_name, email_address, password)

        assert test_user.first_name == remove_extra_spaces(first_name)
        assert test_user.last_name == remove_extra_spaces(last_name)

        test_user.delete_instance()

    @staticmethod
    @given(first_name=text(characters(whitelist_categories=[], whitelist_characters=list(printable))),
           last_name=text(characters(whitelist_categories=[], whitelist_characters=list(printable))),
           email_address=emails(),
           password=text())
    def test_user_instantiation_hashes_password(first_name, last_name, email_address, password):
        test_user = User.instantiate(first_name, last_name, email_address, password)
        assert check_password_hash(test_user.password, password)
        test_user.delete_instance()

    @staticmethod
    @given(first_name=text(characters(whitelist_categories=[], whitelist_characters=list(printable))),
           last_name=text(characters(whitelist_categories=[], whitelist_characters=list(printable))),
           email_address=emails(),
           password=text())
    def test_user_retrieve(first_name, last_name, email_address, password):
        test_user = User.instantiate(first_name, last_name, email_address, password)
        assert User.retrieve(email_address=email_address) == test_user
        test_user.delete_instance()
