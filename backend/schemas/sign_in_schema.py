from werkzeug.security import check_password_hash

from marshmallow import validates_schema, ValidationError, post_load
from marshmallow.fields import String

from models import db
from models.user import User

from schemas.base import Base
from schemas.forbid_blank_str import ForbidBlankStr


class SignInSchema(Base):
    custom_errors = {
        "invalid_credentials": "Invalid credentials. Please try again."
    }

    # will check if email is in db anyway, so
    # marshmallow's Email() field validation isn't needed.
    email_address = String(
        required=True,
        validate=ForbidBlankStr()
    )

    password = String(
        required=True,
        validate=ForbidBlankStr()
    )

    @validates_schema
    def has_valid_credentials(self, data):
        email_address = data.get("email_address")
        password = data.get("password")

        with db:
            user = User.retrieve(email_address)
            if user is None or not check_password_hash(user.password, password):
                raise ValidationError(
                    SignInSchema.custom_errors["invalid_credentials"]
                )

    @post_load
    def get_user_match(self, data):
        return User.retrieve(data["email_address"])
