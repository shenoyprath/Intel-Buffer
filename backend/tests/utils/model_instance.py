from contextlib import contextmanager


@contextmanager
def model_instance(model, *instance_args, **instance_kwargs):
    """
    Context manager for use in test cases to auto create model instance, run some test code, and then destroy instance.
    Useful when one row should not be affecting another row when running a test.
    (Ex: IntegrityError raised when running test that inserts the same email for two users without deleting the first.)

    Note: This is used over a pytest fixture as using a parametrized fixture makes the test case every unreadable and
    hard to integrate with hypothesis's @given decorator.
    """

    instance = model.instantiate(*instance_args, **instance_kwargs)

    # If cleanup is not included in a 'finally' block,
    # pytest will skip cleanup if test/assertion fails
    try:
        yield instance
    finally:
        instance.delete_instance()
