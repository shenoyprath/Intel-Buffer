from werkzeug.security import check_password_hash

from marshmallow import validates_schema, ValidationError
from marshmallow.fields import String

from models import db
from models.user import User

from schemas.base import Base


class LoginSchema(Base):
    # will check for email in db anyway, so marshmallow's email validation is not needed.
    email_address = String()

    password = String()

    errors = {"required": "Your email address and password are required.",
              "invalid_credentials": "Invalid credentials. Please try again."}

    @validates_schema
    def has_valid_credentials(self, data):
        try:
            email_address = data["email_address"]
            password = data["password"]
        except (AttributeError, KeyError):
            raise ValidationError(LoginSchema.errors["required"])

        with db:
            user = User.retrieve(email_address=email_address)
            if user is None or not check_password_hash(user.password, password):
                raise ValidationError(LoginSchema.errors["invalid_credentials"])
