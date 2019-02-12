from hypothesis import given
from hypothesis.strategies import emails, text

from pytest import raises

from marshmallow import ValidationError

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
