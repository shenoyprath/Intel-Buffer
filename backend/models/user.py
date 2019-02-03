from datetime import datetime

from flask_login import UserMixin

from peewee import BooleanField, CharField, DateTimeField, FixedCharField

from models.base import Base


class User(UserMixin, Base):
    first_name = CharField()

    last_name = CharField()

    email_address = CharField(unique=True)

    password = FixedCharField(max_length=80)

    bio = CharField(max_length=160, null=True)  # member's 160 character bio

    creation_timestamp = DateTimeField(default=datetime.utcnow)

    last_login_timestamp = DateTimeField(null=True, default=datetime.utcnow)

    is_verified = BooleanField(default=False)
