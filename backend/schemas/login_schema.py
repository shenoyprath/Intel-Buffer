from werkzeug.security import check_password_hash

from marshmallow import validates_schema, ValidationError
from marshmallow.fields import String

from models import db
from models.user import User

from schemas.base import Base


class LoginSchema(Base):
    custom_errors = {"invalid_credentials": "Invalid credentials. Please try again."}

    email_address = String(required=True)  # will check if email is in db anyway, Email() field validation isn't needed.

    password = String(required=True)

    @validates_schema(skip_on_field_errors=True)
    def has_valid_credentials(self, data):
        email_address = data.get("email_address")
        password = data.get("password")

        with db:
            user = User.retrieve(email_address=email_address)
            if user is None or not check_password_hash(user.password, password):
                raise ValidationError(LoginSchema.custom_errors["invalid_credentials"])
