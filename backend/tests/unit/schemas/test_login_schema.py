from hypothesis import given
from hypothesis.strategies import emails, text

from pytest import fail

from marshmallow import ValidationError

from models.user import User

from schemas.login_schema import LoginSchema

from tests.unit.models.add_and_drop_row import add_and_drop_row
from tests.unit.models.test_database_accessor import DatabaseAccessor
from tests.unit.schemas.get_load_error import get_load_error


class TestLoginSchema(DatabaseAccessor):
    @given(email_address=emails(), password=text())
    def test_invalidates_incorrect_credentials(self, email_address, password):
        e = get_load_error(LoginSchema,
                           {"email_address": email_address,
                            "password": password})

        assert LoginSchema.custom_errors["invalid_credentials"] in e.value.messages["_schema"]

    @given(email_address=emails(), password=text())
    @add_and_drop_row(User, first_name="John", last_name="Doe")  # first & last name are required columns
    def test_validates_correct_credentials(self, row):
        try:
            LoginSchema().load({"email_address": row.email_address,
                                "password": row.password})
        except ValidationError:
            fail("ValidationError was unexpectedly raised.")
