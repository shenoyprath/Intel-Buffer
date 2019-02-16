from functools import wraps


def add_and_drop_row(model, **static_column_values):
    """
    Decorator for test cases to auto create model instance, run test case, and then destroy instance.
    Useful when one row should not be affecting another row when running a test.
    (Ex: IntegrityError raised when running test that inserts the same email for two users without deleting the first.)

    Example of decorator being used with hypothesis's @given decorator:
    @given(some_dynamic_test_value=text())
    @add_and_drop_row(User, static_row_value1="one", static_row_value2="two")
    def test_case(row):

    :param model: Model that is instantiated.
    :param static_column_values: The test case will not focus on these values, but they are required to create the row.
    """

    def decorator(test_case):
        @wraps(test_case)
        def wrapper(**dynamic_column_values):
            """
            :param dynamic_column_values: Dynamically generated (using hypothesis) column values.
            """

            row = model.instantiate(**static_column_values, **dynamic_column_values)
            test_return = test_case(row=row)
            row.delete_instance()
            return test_return

        return wrapper
    return decorator
