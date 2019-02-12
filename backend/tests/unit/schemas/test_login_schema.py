from hypothesis import given
from hypothesis.strategies import emails, text

from pytest import raises, fail

from marshmallow import ValidationError

from models.user import User

from schemas.login_schema import LoginSchema

from tests.unit.models.test_database_accessor import DatabaseAccessor

from tests.test_utils.json_strategy import recursive_json


class TestLoginSchema(DatabaseAccessor):
    @staticmethod
    @given(payload=recursive_json)
    def test_invalidates_no_credentials(payload):
        with raises(ValidationError) as e:
            LoginSchema().load(payload)

        assert LoginSchema.errors["required"] in e.value.messages["_schema"]

    @staticmethod
    @given(email_address=emails(),
           password=text())
    def test_invalidates_incorrect_credentials(email_address, password):
        with raises(ValidationError) as e:
            LoginSchema().load({"email_address": email_address,
                                "password": password})

        assert LoginSchema.errors["invalid_credentials"] in e.value.messages["_schema"]

    @staticmethod
    @given(email_address=emails(),
           password=text())
    def test_validates_correct_credentials(email_address, password):
        name = " "  # database will not store null value for first_name and last_name columns
        test_user = User.instantiate(first_name=name,
                                     last_name=name,
                                     email_address=email_address,
                                     password=password)

        try:
            LoginSchema().load({"email_address": email_address,
                                "password": password})
        except ValidationError:
            fail("ValidationError was unexpectedly raised.")

        test_user.delete_instance()  # clean up so that IntegrityError does not get raised if same email is used again.
