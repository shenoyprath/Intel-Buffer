from pytest import mark

from hypothesis import given
from hypothesis.strategies import emails, text

from models.user import User

from schemas.sign_in_schema import SignInSchema

from tests.utils.model_instance import model_instance


@mark.usefixtures("database")
class TestSignInSchema:
    @given(email_address=emails())
    def test_invalidates_nonexistent_email_address(self, email_address):
        errors = SignInSchema().validate({
            "email_address": email_address,
            "password": "Password123"
        })

        assert SignInSchema.custom_errors["nonexistent_email"] in errors["email_address"]

    @given(
        email_address=emails(),
        password=text(min_size=1),
        incorrect_password=text(min_size=1)
    )
    def test_invalidates_incorrect_password_for_existing_email_address(
        self, email_address, password, incorrect_password
    ):
        with model_instance(
            User,
            first_name="Jane",
            last_name="Doe",
            email_address=email_address,
            password=password
        ):
            errors = SignInSchema().validate({
                "email_address": email_address,
                "password": password + incorrect_password  # in case both have the same value.
            })

        assert SignInSchema.custom_errors["incorrect_password"] in errors["password"]

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
