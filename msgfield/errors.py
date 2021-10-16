class ValidateFieldErr(Exception):
    def __init__(self, field_name):
        self.field_name = field_name


class RequiredFieldErr(ValidateFieldErr):
    pass


__all__ = ['RequiredFieldErr']
