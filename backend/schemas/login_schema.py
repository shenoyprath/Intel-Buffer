from marshmallow.fields import String

from schemas.base import Base


class LoginSchema(Base):
    # will check for email in db anyway, so marshmallow's email validation is not needed
    email_address = String()

    password = String()

    errors = {"required": "Your email address and password are required.",
              "invalid_credentials": "Invalid credentials. Please try again."}
