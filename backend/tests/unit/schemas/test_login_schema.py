from hypothesis import given
from hypothesis.strategies import emails, text

from pytest import mark

from models.user import User

from schemas.login_schema import LoginSchema

from tests.unit.models.model_instance import model_instance


@mark.usefixtures("database")
class TestLoginSchema:
    @given(email_address=emails(), password=text())
    def test_invalidates_incorrect_credentials(self, email_address, password):
        errors = LoginSchema().validate({
            "email_address": email_address,
            "password": password
        })

        assert LoginSchema.custom_errors["invalid_credentials"] in errors["_schema"]

    @given(email_address=emails(), password=text(min_size=1))
    def test_validates_correct_credentials(self, email_address, password):
        with model_instance(
            User,
            first_name="John",
            last_name="Doe",
            email_address=email_address,
            password=password
        ):
            errors = LoginSchema().validate({
                "email_address": email_address,
                "password": password
            })
        assert not errors
