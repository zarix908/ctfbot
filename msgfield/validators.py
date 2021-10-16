from msgfield.errors import RequiredFieldErr


def with_raise(err_class):
    def decorator(func):
        def new_func(field_name, *args, **kwargs):
            if not func(*args, **kwargs):
                raise err_class(field_name)

        return new_func

    return decorator


@with_raise(RequiredFieldErr)
def required(value):
    return bool(value)
