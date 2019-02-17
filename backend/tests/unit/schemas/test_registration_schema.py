from hypothesis import given
from hypothesis.strategies import text, one_of, characters, emails

from pytest import fail, mark

from marshmallow import ValidationError

from models.user import User

from schemas.registration_schema import RegistrationSchema

from tests.unit.models.model_instance import model_instance
from tests.unit.schemas.get_load_error import get_load_error


@mark.usefixtures("database_accessor")
class TestRegistrationSchema:
    @given(email_address=emails())
    def test_invalidates_existing_email(self, email_address):
        with model_instance(User,
                            first_name="John",
                            last_name="Doe",
                            email_address=email_address,
                            password="Password123") as test_user:
            e = get_load_error(RegistrationSchema,
                               {"email_address": test_user.email_address})

        assert RegistrationSchema.custom_errors["email_exists"] in e.value.messages["email_address"]

    @given(password=one_of(text(characters(blacklist_categories=("L",))),  # blacklist letters
                           text(characters(blacklist_categories=("N",)))))  # blacklist numbers
    def test_invalidates_password_without_letters_or_nums(self, password):
        e = get_load_error(RegistrationSchema, {"password": password})
        assert RegistrationSchema.custom_errors["password_req_chars"] in e.value.messages["password"]

    @given(email_address=emails())
    def test_invalidates_password_matching_email(self, email_address):
        e = get_load_error(RegistrationSchema,
                           {"email_address": email_address,
                            "password": email_address})
        assert RegistrationSchema.custom_errors["password_is_email"] in e.value.messages["password"]

    @given(name=text(characters(blacklist_categories=("C", "Z")), min_size=1),  # whitespace is categorized as C or Z.
           email_address=emails(),
           password=text(characters(whitelist_categories=("L", "N")),
                         min_size=RegistrationSchema.min_password_len,
                         max_size=RegistrationSchema.max_password_len))
    def test_validates_when_all_criteria_meet(self, name, email_address, password):
        try:
            RegistrationSchema().load({"first_name": name,
                                       "last_name": name,
                                       "email_address": email_address,
                                       "password": password})
        except ValidationError as e:
            fail(str(e))
