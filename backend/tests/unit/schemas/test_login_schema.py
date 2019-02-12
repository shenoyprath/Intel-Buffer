from hypothesis import given

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
