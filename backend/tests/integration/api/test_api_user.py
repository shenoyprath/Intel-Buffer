from pytest import mark


# file named test_api_user to avoid pytest conflict with test_user from unit/models.
@mark.usefixtures("database")
class TestUser:

    endpoint = "api.user"
