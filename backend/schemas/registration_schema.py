from marshmallow import ValidationError, validates, validates_schema
from marshmallow.fields import String, Email
from marshmallow.validate import Length

from models.user import User

from schemas.base import Base

from utils.is_empty_or_space import is_empty_or_space


class RegistrationSchema(Base):
    # TODO: find a way to change the default error messages for all fields without having to pass arguments repeatedly
    custom_errors = {"required": "This field is required."}

    first_name = String(required=True, error_messages=custom_errors)

    last_name = String(required=True, error_messages=custom_errors)

    email_address = Email(required=True, error_messages=custom_errors)

    password_len_msg = "Password must be between {min} and {max} characters long."
    password_req_chars_msg = "Password must contain letters and numbers."
    password_is_email_msg = "Password cannot be the same as your email address."
    password = String(required=True,
                      error_messages=custom_errors,
                      validate=Length(min=User.min_password_len,
                                      max=User.max_password_len,
                                      error=password_len_msg))

    @validates("password")
    def has_letters_and_nums(self, password):
        has_letters = any(char.isalpha() for char in password)
        has_numbers = any(char.isdigit() for char in password)

        if not has_letters or not has_numbers:
            raise ValidationError(RegistrationSchema.password_req_chars_msg)

    @validates_schema
    def names_are_not_spaces(self, data):
        field_required_msg = RegistrationSchema.custom_errors["required"]

        first_name = data.get("first_name")
        if first_name is not None and is_empty_or_space(first_name):
            raise ValidationError(field_required_msg, field_names=["first_name"])

        last_name = data.get("last_name")
        if last_name is not None and is_empty_or_space(last_name):
            raise ValidationError(field_required_msg, field_names=["last_name"])

    @validates_schema
    def password_is_not_email(self, data):
        if data.get("password") == data.get("email_address"):
            raise ValidationError(message=RegistrationSchema.password_is_email_msg,
                                  field_names=["password"])
