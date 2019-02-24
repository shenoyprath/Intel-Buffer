from werkzeug.security import check_password_hash

from pytest import mark

from hypothesis import given
from hypothesis.strategies import text

from models.user import User

from utils.remove_extra_spaces import remove_extra_spaces

from tests.utils.model_instance import model_instance


@mark.usefixtures("database")
class TestUser:
    @given(first_name=text(), last_name=text())
    def test_user_instantiation_removes_extra_spaces_in_names(self, first_name, last_name):
        with model_instance(
            User,
            first_name=first_name,
            last_name=last_name,
            email_address="example@example.com",
            password="Password123"
        ) as test_user:
            assert test_user.first_name == remove_extra_spaces(first_name)
            assert test_user.last_name == remove_extra_spaces(last_name)

    @given(password=text())
    def test_user_instantiation_hashes_password(self, password):
        with model_instance(
            User,
            first_name="John",
            last_name="Doe",
            email_address="example@example.com",
            password=password
        ) as test_user:
            assert check_password_hash(test_user.password, password)
