from werkzeug.security import check_password_hash

from marshmallow import validates_schema, ValidationError
from marshmallow.fields import String

from models import db
from models.user import User

from schemas.base import Base


class LoginSchema(Base):
    # will check for email in db anyway, so marshmallow's email validation is not needed.
    email_address = String(required=True)

    password = String(required=True)

    custom_errors = {"invalid_credentials": "Invalid credentials. Please try again."}

    @validates_schema
    def has_valid_credentials(self, data):
        email_address = data.get("email_address")
        password = data.get("password")

        with db:
            user = User.retrieve(email_address=email_address)
            if user is None or not check_password_hash(user.password, password):
                raise ValidationError(LoginSchema.custom_errors["invalid_credentials"])
