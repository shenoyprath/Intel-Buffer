from werkzeug.security import check_password_hash

from hypothesis import given
from hypothesis.strategies import text, emails

from pytest import mark

from models.user import User

from utils.remove_extra_spaces import remove_extra_spaces


@mark.usefixtures("database_accessor")
class TestUser:
    @given(first_name=text(),
           last_name=text(),
           email_address=emails(),
           password=text())
    def test_user_instantiation_removes_extra_spaces_in_names(self, first_name, last_name, email_address, password):
        test_user = User.instantiate(first_name, last_name, email_address, password)

        assert test_user.first_name == remove_extra_spaces(first_name)
        assert test_user.last_name == remove_extra_spaces(last_name)

        test_user.delete_instance()

    @given(first_name=text(),
           last_name=text(),
           email_address=emails(),
           password=text())
    def test_user_instantiation_hashes_password(self, first_name, last_name, email_address, password):
        test_user = User.instantiate(first_name, last_name, email_address, password)
        assert check_password_hash(test_user.password, password)
        test_user.delete_instance()
