from werkzeug.security import generate_password_hash

from peewee import BooleanField, CharField

from models.base import Base

from utils.remove_extra_spaces import remove_extra_spaces


class User(Base):
    first_name = CharField()

    last_name = CharField()

    email_address = CharField(unique=True)

    password = CharField()

    bio = CharField(max_length=160, null=True)  # user's 160 character bio

    is_verified = BooleanField(default=False)

    @classmethod
    def instantiate(cls, first_name, last_name, email_address, password):
        first_name, last_name = (remove_extra_spaces(name) for name in (first_name, last_name))
        hashed_password = generate_password_hash(password=password, method="sha256")

        return cls.create(
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            password=hashed_password
        )

    @classmethod
    def retrieve(cls, email_address):
        return cls.get_or_none(cls.email_address == email_address)

    def __repr__(self):
        return "\n".join([
            f"First Name: {self.first_name}",
            f"Last Name: {self.last_name}",
            f"Email Address: {self.email_address}"
        ])
