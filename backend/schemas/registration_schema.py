from marshmallow import ValidationError, validates, validates_schema
from marshmallow.fields import String, Email
from marshmallow.validate import Length

from models import db
from models.user import User

from schemas.base import Base
from schemas.forbid_blank_str import ForbidBlankStr

from utils.has_alphanum_chars import has_alphanum_chars


class RegistrationSchema(Base):
    custom_errors = {
        "email_exists": "Email address already exists.",
        "password_len": "Password must be between {min} and {max} characters long.",
        "password_req_chars": "Password must contain letters and numbers.",
        "password_is_email": "Password cannot be the same as your email address."
    }

    first_name = String(
        required=True,
        allow_none=False,
        validate=ForbidBlankStr(forbid_whitespace_str=True)
    )

    last_name = String(
        required=True,
        allow_none=False,
        validate=ForbidBlankStr(forbid_whitespace_str=True)
    )

    email_address = Email(required=True, allow_none=False)

    min_password_len, max_password_len = 8, 50
    password = String(
        required=True,
        allow_none=False,
        validate=Length(
            min=min_password_len,
            max=max_password_len,
            error=custom_errors["password_len"]
        )
    )

    @validates("email_address")
    def is_unique(self, email_address):
        with db:
            if User.retrieve(email_address) is not None:
                raise ValidationError(
                    RegistrationSchema.custom_errors["email_exists"]
                )

    @validates("password")
    def has_letters_and_nums(self, password):
        if not has_alphanum_chars(password):
            raise ValidationError(
                RegistrationSchema.custom_errors["password_req_chars"]
            )

    @validates_schema
    def password_is_not_email(self, data):
        if data.get("password") == data.get("email_address"):
            raise ValidationError(
                message=RegistrationSchema.custom_errors["password_is_email"],
                field_names=["password"]
            )
