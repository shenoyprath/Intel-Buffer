from pytest import mark

from hypothesis import given
from hypothesis.strategies import emails, text

from models.user import User

from schemas.sign_in_schema import SignInSchema

from tests.utils.model_instance import model_instance


@mark.usefixtures("database")
class TestLoginSchema:
    @given(email_address=emails(), password=text(min_size=1))
    def test_invalidates_incorrect_credentials(self, email_address, password):
        errors = SignInSchema().validate({
            "email_address": email_address,
            "password": password
        })

        assert SignInSchema.custom_errors["invalid_credentials"] in errors["_schema"]

    @given(email_address=emails(), password=text(min_size=1))
    def test_validates_correct_credentials_and_loads_user(self, email_address, password):
        with model_instance(
            User,
            first_name="John",
            last_name="Doe",
            email_address=email_address,
            password=password
        ) as test_user:
            credentials = {
                "email_address": email_address,
                "password": password
            }
            errors = SignInSchema().validate(credentials)
            user = SignInSchema().load(credentials)

        assert not errors
        assert test_user == user
