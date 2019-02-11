from string import printable, whitespace, ascii_letters

from hypothesis import given, example, assume
from hypothesis.strategies import text, dictionaries, one_of, characters, emails, integers, data, booleans, \
                                  lists, recursive, floats

from pytest import raises, fail

from marshmallow import ValidationError

from models.user import User

from schemas.registration_schema import RegistrationSchema

from tests.unit.models.test_database_accessor import DatabaseAccessor


class TestRegistrationSchema(DatabaseAccessor):
    required_msg = RegistrationSchema.custom_errors["required"]

    recursive_json = recursive(booleans() |
                               floats() |
                               text(printable),
                               lambda children: lists(children, 1) |
                               dictionaries(text(printable), children, min_size=1))  # straight out of the docs

    @staticmethod
    def get_load_error(payload):
        with raises(ValidationError) as e:
            RegistrationSchema().load(payload)
        return e

    @staticmethod
    @given(payload=recursive_json)
    @example({})
    def test_invalidates_nonexistence_of_required_fields(payload):
        e = TestRegistrationSchema.get_load_error(payload)

        if isinstance(payload, dict):
            assert all(TestRegistrationSchema.required_msg in e.value.messages[field]
                       for field in ("first_name", "last_name", "email_address", "password"))
        else:
            assert "Invalid input type." in e.value.messages["_schema"]

    whitespace_name = text(characters(whitelist_categories=(),
                                      whitelist_characters=list(whitespace)))

    @staticmethod
    @given(first_name=whitespace_name, last_name=whitespace_name)
    def test_invalidates_empty_or_whitespace_names(first_name, last_name):
        payload = {"first_name": first_name,
                   "last_name": last_name}
        e = TestRegistrationSchema.get_load_error(payload)

        fields = ("first_name", "last_name")
        assert all(field in e.value.messages for field in fields)
        assert all(TestRegistrationSchema.required_msg in e.value.messages[field]
                   for field in ("first_name", "last_name"))

    @staticmethod
    @given(text())
    def test_invalidates_invalid_email(invalid_email):
        e = TestRegistrationSchema.get_load_error({"email_address": invalid_email})

        assert "email_address" in e.value.messages
        assert "Not a valid email address." in e.value.messages["email_address"]

    used_emails = []

    @staticmethod
    @given(first_name=text(characters(whitelist_characters=list(printable), whitelist_categories=()), min_size=1),
           last_name=text(characters(whitelist_characters=list(printable), whitelist_categories=()), min_size=1),
           email_address=emails().filter(lambda email: email not in TestRegistrationSchema.used_emails),
           password=data())
    def test_invalidates_existing_email(first_name, last_name, email_address, password):
        password_nums = password.draw(integers())
        password_letters = password.draw(text(characters(whitelist_categories=(),
                                                         whitelist_characters=list(ascii_letters)), min_size=1))
        password = str(password_nums) + password_letters
        assume(RegistrationSchema.min_password_len < len(password) < RegistrationSchema.max_password_len)

        User.instantiate(first_name, last_name, email_address, password)
        TestRegistrationSchema.used_emails.append(email_address)
        payload_dict = {"first_name": first_name,
                        "last_name": last_name,
                        "email_address": email_address,
                        "password": password}

        e = TestRegistrationSchema.get_load_error(payload_dict)
        assert "email_address" in e.value.messages
        assert e.value.messages["email_address"]

    @staticmethod
    @given(password=one_of(text(min_size=RegistrationSchema.max_password_len + 1),
                           text(max_size=RegistrationSchema.min_password_len - 1)))
    def test_invalidates_password_len_out_of_range(password):
        e = TestRegistrationSchema.get_load_error({"password": password})
        password_len_msg = RegistrationSchema.password_len_msg \
                                             .format(min=RegistrationSchema.min_password_len,
                                                     max=RegistrationSchema.max_password_len)

        assert "password" in e.value.messages
        assert password_len_msg in e.value.messages["password"]

    @staticmethod
    @given(password=one_of(text(characters(blacklist_categories=["L"])),  # blacklist letters
                           text(characters(blacklist_categories=["N"])),  # blacklist numbers
                           text(characters(blacklist_categories=["L", "N"])))
           .filter(lambda password: RegistrationSchema.min_password_len <
                   len(password) <
                   RegistrationSchema.max_password_len))
    def test_invalidates_password_without_letters_or_nums(password):
        e = TestRegistrationSchema.get_load_error({"password": password})

        assert "password" in e.value.messages
        assert RegistrationSchema.password_req_chars_msg in e.value.messages["password"]

    @staticmethod
    @given(strategy=data())
    def test_invalidates_password_matching_email(strategy):
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
        e = TestRegistrationSchema.get_load_error(payload)

        assert "password" in e.value.messages
        assert RegistrationSchema.password_is_email_msg in e.value.messages["password"]

    @staticmethod
    @given(first_name=text(characters(blacklist_categories=("C", "Z")), min_size=1),
           last_name=text(characters(blacklist_categories=("C", "Z")), min_size=1),
           email_address=emails(),
           password=data())
    def test_validates_when_all_criteria_meet(first_name, last_name, email_address, password):
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
