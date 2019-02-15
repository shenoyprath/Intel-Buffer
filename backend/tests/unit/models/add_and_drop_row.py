from functools import wraps


def add_and_drop_row(model, **column_values):
    """
    Decorator for test cases to auto create model instance, run test case, and then destroy instance.
    Useful when one row should not be affecting another row when running a test.
    (Ex: IntegrityError raised when running test that inserts the same email for two users without deleting the first.)
    """

    def decorator(test_case):
        @wraps(test_case)
        def wrapper(*args, **kwargs):
            row = model.instantiate(**column_values)
            test_return = test_case(*args, **kwargs)
            row.delete_instance()
            return test_return

        return wrapper
    return decorator
