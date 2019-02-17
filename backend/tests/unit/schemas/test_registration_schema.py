from hypothesis import given
from hypothesis.strategies import text, one_of, characters, emails

from pytest import mark

from models.user import User

from schemas.registration_schema import RegistrationSchema

from tests.unit.models.model_instance import model_instance


@mark.usefixtures("database_accessor")
class TestRegistrationSchema:
    @given(email_address=emails())
    def test_invalidates_existing_email(self, email_address):
        with model_instance(User,
                            first_name="John",
                            last_name="Doe",
                            email_address=email_address,
                            password="Password123") as test_user:
            errors = RegistrationSchema().validate({"email_address": test_user.email_address})

        assert RegistrationSchema.custom_errors["email_exists"] in errors["email_address"]

    @given(password=one_of(text(characters(blacklist_categories=("L",))),  # blacklist letters
                           text(characters(blacklist_categories=("N",)))))  # blacklist numbers
    def test_invalidates_password_without_letters_or_nums(self, password):
        errors = RegistrationSchema().validate({"password": password})
        assert RegistrationSchema.custom_errors["password_req_chars"] in errors["password"]

    @given(email_address=emails())
    def test_invalidates_password_matching_email(self, email_address):
        errors = RegistrationSchema().validate({"email_address": email_address,
                                                "password": email_address})
        assert RegistrationSchema.custom_errors["password_is_email"] in errors["password"]

    @given(name=text(characters(blacklist_categories=("C", "Z")), min_size=1),  # whitespace is categorized as C or Z.
           email_address=emails(),
           password=text(characters(whitelist_categories=("L", "N")),
                         min_size=RegistrationSchema.min_password_len,
                         max_size=RegistrationSchema.max_password_len))
    def test_validates_when_all_criteria_meet(self, name, email_address, password):
        errors = RegistrationSchema().validate({"first_name": name,
                                                "last_name": name,
                                                "email_address": email_address,
                                                "password": password})
        assert not errors
