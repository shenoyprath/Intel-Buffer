from marshmallow.fields import String, Email
from marshmallow.validate import Length

from models.user import User

from schemas.base import Base


class RegistrationSchema(Base):
    first_name = String(required=True)

    last_name = String(required=True)

    email_address = Email(required=True)

    password = String(required=True,
                      validate=Length(min=User.min_password_len,
                                      max=User.max_password_len,
                                      error="Password must be between {min} and {max} characters long."))
