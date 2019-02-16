from marshmallow import ValidationError, validates, validates_schema
from marshmallow.fields import Field, String, Email
from marshmallow.validate import Length

from models import db
from models.user import User

from schemas.base import Base

from utils.is_empty_or_space import is_empty_or_space


class RegistrationSchema(Base):
    custom_errors = {"email_exists": "Email address already exists.",
                     "password_len": "Password must be between {min} and {max} characters long.",
                     "password_req_chars": "Password must contain letters and numbers.",
                     "password_is_email": "Password cannot be the same as your email address."}

    first_name = String(required=True)

    last_name = String(required=True)

    email_address = Email(required=True)

    min_password_len, max_password_len = 8, 50
    password = String(required=True,
                      validate=Length(min=min_password_len,
                                      max=max_password_len,
                                      error=custom_errors["password_len"]))

    @validates("email_address")
    def is_unique(self, email_address):
        with db:
            if User.retrieve(email_address) is not None:
                raise ValidationError(RegistrationSchema.custom_errors["email_exists"])

    @validates("password")
    def has_letters_and_nums(self, password):
        has_letters = any(char.isalpha() for char in password)
        has_numbers = any(char.isdigit() for char in password)

        if not has_letters or not has_numbers:
            raise ValidationError(RegistrationSchema.custom_errors["password_req_chars"])

    @validates_schema
    def names_are_not_spaces(self, data):
        blank_fields = []
        for field_name in ("first_name", "last_name"):
            field_value = data.get(field_name)
            # short circuit None value as it's handled by marshmallow's required parameter.
            if field_value is not None and is_empty_or_space(field_value):
                blank_fields.append(field_name)

        if blank_fields:
            raise ValidationError(Field.default_error_messages["required"],
                                  field_names=blank_fields)

    @validates_schema
    def password_is_not_email(self, data):
        if data.get("password") == data.get("email_address"):
            raise ValidationError(message=RegistrationSchema.custom_errors["password_is_email"],
                                  field_names=["password"])
