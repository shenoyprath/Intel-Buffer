from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from peewee import BooleanField, CharField, DateTimeField, FixedCharField

from models.base import Base
from utils.remove_extra_spaces import remove_extra_spaces


class User(UserMixin, Base):
    first_name = CharField()

    last_name = CharField()

    email_address = CharField(unique=True)

    password = FixedCharField(max_length=80)

    bio = CharField(max_length=160, null=True)  # user's 160 character bio

    creation_timestamp = DateTimeField(default=datetime.utcnow)

    last_login_timestamp = DateTimeField(null=True, default=datetime.utcnow)

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
