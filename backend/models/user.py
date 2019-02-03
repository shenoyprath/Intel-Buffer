from datetime import datetime

from werkzeug.security import generate_password_hash

from peewee import BooleanField, CharField, DateTimeField, FixedCharField

from models.base import Base
from utils.remove_extra_spaces import remove_extra_spaces


class User(Base):
    first_name = CharField()

    last_name = CharField()

    email_address = CharField(unique=True)

    password = FixedCharField(max_length=80)

    bio = CharField(max_length=160, null=True)  # user's 160 character bio

    is_verified = BooleanField(default=False)

    @classmethod
    def instantiate(cls, first_name, last_name, email_address, password):
        first_name, last_name = remove_extra_spaces(first_name, last_name)
        hashed_password = generate_password_hash(password=password, method="sha256")

        return cls.create(
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            password=hashed_password
        )

    @classmethod
    def retrieve(cls, **kwargs):
        email_address = kwargs.get("email_address")
        if email_address is not None:
            return cls.get_or_none(cls.email_address == email_address)
        return super().retrieve(identity=kwargs.get("identity"))

    def __repr__(self):
        return (
            f"First Name: {self.first_name} \n"
            f"Last Name: {self.last_name} \n"
            f"Email Address: {self.email_address}"
        )
