from string import printable, ascii_letters

from hypothesis import given, example, assume
from hypothesis.strategies import text, dictionaries, recursive, booleans, floats, lists, one_of, characters, emails, \
                                  integers, data

from pytest import raises, fail

from marshmallow import ValidationError

from models.user import User

from schemas.registration_schema import RegistrationSchema


class TestRegistrationSchema:
    json_strategy = recursive(booleans() |
                              floats() |
                              text(printable),
                              lambda children: lists(children, 1) |
                              dictionaries(text(printable), children, min_size=1))  # straight out of the docs

    required_msg = RegistrationSchema.custom_errors["required"]

    password_len_msg = RegistrationSchema.password_len_msg \
                                         .format(min=User.min_password_len, max=User.max_password_len)

    @staticmethod
    @given(payload=json_strategy)
    @example({})
    def test_invalidates_nonexistence_of_required_fields(payload):
        with raises(ValidationError) as e:
            RegistrationSchema().load(payload)

        required_msg = TestRegistrationSchema.required_msg
        if isinstance(payload, dict):
            for field in ("first_name", "last_name", "email_address", "password"):
                assert required_msg in e.value.messages[field]
        else:
            assert "Invalid input type." in e.value.messages["_schema"]

    @staticmethod
    def test_invalidates_empty_or_whitespace_names():
        pass

    @staticmethod
    @given(text())
    def test_invalidates_invalid_email(invalid_email):
        payload_dict = {"email_address": invalid_email}
        with raises(ValidationError) as e:
            RegistrationSchema().load(payload_dict)

        assert "email_address" in e.value.messages
        assert "Not a valid email address." in e.value.messages["email_address"]

    @staticmethod
    @given(password=one_of(text(min_size=User.max_password_len + 1),
                           text(max_size=User.min_password_len - 1)))
    def test_invalidates_password_len_out_of_range(password):
        password_dict = {"password": password}
        with raises(ValidationError) as e:
            RegistrationSchema().load(password_dict)

        assert "password" in e.value.messages
        assert TestRegistrationSchema.password_len_msg in e.value.messages["password"]

    @staticmethod
    @given(password=one_of(text(characters(blacklist_categories=["L"]),
                                min_size=User.min_password_len,
                                max_size=User.max_password_len),
                           text(characters(blacklist_categories=["N"]),
                                min_size=User.min_password_len,
                                max_size=User.max_password_len)))
    def test_invalidates_password_without_letters_or_nums(password):
        password_dict = {"password": password}
        with raises(ValidationError) as e:
            RegistrationSchema().load(password_dict)

        assert "password" in e.value.messages
        assert RegistrationSchema.password_req_chars_msg in e.value.messages["password"]

    @staticmethod
    @given(strategy=data())
    def test_invalidates_password_matching_email(strategy):
        random_int = strategy.draw(integers())

        def filter_by_len(email):  # filter to pass password length validation
            return User.min_password_len < len(email) + len(str(random_int)) < User.max_password_len

        email_address = strategy.draw(emails()
                                      .filter(lambda email: filter_by_len(email)))
        # integer added to circumvent validation that checks for numbers & letters in passwords
        email_address = str(random_int) + email_address

        payload_dict = {"email_address": email_address,
                        "password": email_address}
        with raises(ValidationError) as e:
            RegistrationSchema().load(payload_dict)

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
        assume(User.min_password_len < len(password) < User.max_password_len)

        payload_dict = {"first_name": first_name,
                        "last_name": last_name,
                        "email_address": email_address,
                        "password": password}
        try:
            RegistrationSchema().load(payload_dict)
        except ValidationError:
            fail(f"ValidationError was unexpectedly raised.")
