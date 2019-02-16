from contextlib import contextmanager


@contextmanager
def model_instance(model, *instance_args, **instance_kwargs):
    """
    Context manager for use in test cases to auto create model instance, run test case, and then destroy instance.
    Useful when one row should not be affecting another row when running a test.
    (Ex: IntegrityError raised when running test that inserts the same email for two users without deleting the first.)
    """

    instance = model.instantiate(*instance_args, **instance_kwargs)
    yield instance
    instance.delete_instance()
