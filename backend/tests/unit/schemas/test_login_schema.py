from hypothesis import given
from hypothesis.strategies import emails, text

from pytest import fail, mark

from marshmallow import ValidationError

from models.user import User

from schemas.login_schema import LoginSchema

from tests.unit.models.model_instance import model_instance
from tests.unit.schemas.get_load_error import get_load_error


@mark.usefixtures("database_accessor")
class TestLoginSchema:
    @given(email_address=emails(), password=text())
    def test_invalidates_incorrect_credentials(self, email_address, password):
        e = get_load_error(LoginSchema,
                           {"email_address": email_address,
                            "password": password})

        assert LoginSchema.custom_errors["invalid_credentials"] in e.value.messages["_schema"]

    @given(email_address=emails(), password=text())
    def test_validates_correct_credentials(self, email_address, password):
        with model_instance(User,
                            first_name="John",
                            last_name="Doe",
                            email_address=email_address,
                            password=password):
            try:
                LoginSchema().load({"email_address": email_address,
                                    "password": password})
            except ValidationError as e:
                fail(str(e))
