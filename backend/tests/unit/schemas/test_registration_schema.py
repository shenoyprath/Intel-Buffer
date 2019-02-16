from string import whitespace, ascii_letters

from hypothesis import given, assume, example
from hypothesis.strategies import text, one_of, characters, emails, integers, data

from pytest import fail, mark

from marshmallow import ValidationError
from marshmallow.fields import Field

from models.user import User

from schemas.registration_schema import RegistrationSchema

from tests.unit.models.model_instance import model_instance
from tests.unit.schemas.get_load_error import get_load_error


@mark.usefixtures("database_accessor")
class TestRegistrationSchema:
    @given(name=text(characters(whitelist_categories=(),
                                whitelist_characters=list(whitespace))))
    @example("")
    def test_invalidates_empty_or_whitespace_names(self, name):
        e = get_load_error(RegistrationSchema, {"first_name": name,
                                                "last_name": name})
        for field in "first_name", "last_name":
            assert Field.default_error_messages["required"] in e.value.messages[field]

    @given(email_address=emails())
    def test_invalidates_existing_email(self, email_address):
        with model_instance(User,
                            first_name="John",
                            last_name="Doe",
                            email_address=email_address,
                            password="Password123") as test_user:
            e = get_load_error(RegistrationSchema, {"email_address": test_user.email_address})
        assert RegistrationSchema.custom_errors["email_exists"] in e.value.messages["email_address"]

    @given(password=one_of(text(characters(blacklist_categories=["L"])),  # blacklist letters
                           text(characters(blacklist_categories=["N"])),  # blacklist numbers
                           text(characters(blacklist_categories=["L", "N"])))
           .filter(lambda password: RegistrationSchema.min_password_len <
                   len(password) <
                   RegistrationSchema.max_password_len))
    def test_invalidates_password_without_letters_or_nums(self, password):
        e = get_load_error(RegistrationSchema,
                           {"password": password})

        assert "password" in e.value.messages
        assert RegistrationSchema.custom_errors["password_req_chars"] in e.value.messages["password"]

    @given(strategy=data())
    def test_invalidates_password_matching_email(self, strategy):
        random_int = strategy.draw(integers())

        def filter_by_len(email):  # filter to pass password length validation
            return RegistrationSchema.min_password_len < len(email) + len(str(random_int)) < \
                   RegistrationSchema.max_password_len

        email_address = strategy.draw(emails()
                                      .filter(lambda email: filter_by_len(email)))
        # integer added to circumvent validation that checks for numbers & letters in passwords
        email_address = str(random_int) + email_address

        payload = {"email_address": email_address,
                   "password": email_address}
        e = get_load_error(RegistrationSchema, payload)

        assert "password" in e.value.messages
        assert RegistrationSchema.custom_errors["password_is_email"] in e.value.messages["password"]

    @given(first_name=text(characters(blacklist_categories=("C", "Z")), min_size=1),
           last_name=text(characters(blacklist_categories=("C", "Z")), min_size=1),
           email_address=emails(),
           password=data())
    def test_validates_when_all_criteria_meet(self, first_name, last_name, email_address, password):
        password_nums = password.draw(integers())
        password_letters = password.draw(text(characters(whitelist_categories=(),
                                                         whitelist_characters=list(ascii_letters)), min_size=1))
        password = str(password_nums) + password_letters
        assume(RegistrationSchema.min_password_len < len(password) < RegistrationSchema.max_password_len)

        payload_dict = {"first_name": first_name,
                        "last_name": last_name,
                        "email_address": email_address,
                        "password": password}
        try:
            RegistrationSchema().load(payload_dict)
        except ValidationError:
            fail(f"ValidationError was unexpectedly raised.")
