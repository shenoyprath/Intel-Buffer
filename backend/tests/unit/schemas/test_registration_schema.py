from string import whitespace

from pytest import mark

from hypothesis import given
from hypothesis.strategies import text, one_of, characters, emails

from models.user import User

from schemas.registration_schema import RegistrationSchema

from utils.has_alphanum_chars import has_alphanum_chars

from tests.utils.model_instance import model_instance


@mark.usefixtures("database")
class TestRegistrationSchema:
    @given(email_address=emails())
    def test_invalidates_existing_email(self, email_address):
        with model_instance(  # nosec make bandit ignore hardcoded password.
            User,
            first_name="John",
            last_name="Doe",
            email_address=email_address,
            password="Password123"
        ) as test_user:
            errors = RegistrationSchema().validate({
                "email_address": test_user.email_address
            })

        assert RegistrationSchema.custom_errors["email_exists"] in errors["email_address"]

    @given(
        password=one_of(
            text(
                characters(blacklist_categories=("L",)),  # blacklist letters
                min_size=RegistrationSchema.min_password_len,
                max_size=RegistrationSchema.max_password_len
            ),
            text(
                characters(blacklist_categories=("N",)),  # blacklist numbers
                min_size=RegistrationSchema.min_password_len,
                max_size=RegistrationSchema.max_password_len
            )
        )
    )
    def test_invalidates_password_without_letters_or_nums(self, password):
        errors = RegistrationSchema().validate({
            "password": password
        })
        assert RegistrationSchema.custom_errors["password_req_chars"] in errors["password"]

    @given(email_address=emails().filter(
        lambda addr:
            RegistrationSchema.min_password_len <= len(addr) <= RegistrationSchema.max_password_len and
            has_alphanum_chars(addr)
    ))
    def test_invalidates_password_matching_email(self, email_address):
        errors = RegistrationSchema().validate({
            # names given as skip_on_field_errors is True,
            # so @validates_schema won't run if required fields are missing
            "first_name": "John",
            "last_name": "Doe",
            "email_address": email_address,
            "password": email_address
        })
        assert RegistrationSchema.custom_errors["password_is_email"] in errors["password"]

    @given(
        name=text(
            characters(
                blacklist_characters=tuple(whitespace),
                blacklist_categories=("C",)  # no need to test this category
            ),
            min_size=1
        ),
        email_address=emails(),
        password=text(
            min_size=RegistrationSchema.min_password_len,
            max_size=RegistrationSchema.max_password_len
        ).filter(lambda password: has_alphanum_chars(password))
    )
    def test_validates_when_all_criteria_meet_and_loads_user(self, name, email_address, password):
        credentials = {
            "first_name": name,
            "last_name": name,
            "email_address": email_address,
            "password": password
        }
        errors = RegistrationSchema().validate(credentials)
        assert not errors

        new_user = RegistrationSchema().load(credentials)
        for attr, val in credentials.items():
            if attr != "password":  # password gets hashed
                assert getattr(new_user, attr) == val
        new_user.delete_instance()  # clean up to avoid IntegrityError
