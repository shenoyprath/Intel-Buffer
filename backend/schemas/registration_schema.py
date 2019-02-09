from marshmallow.fields import String, Email

from schemas.base import Base


class RegistrationSchema(Base):
    first_name = String(required=True)

    last_name = String(required=True)

    email_address = Email(required=True)

    password = String(required=True)
