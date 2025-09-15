from common.errors.validation import ValidationErrors


def min_length(min_: int, error=None):
    def validator(value, field_name: str):
        if not isinstance(value, str):
            return ValidationErrors.NOT_STRING.for_field(field_name).to_dict()
        if len(value) < min_:
            err = error or ValidationErrors.MIN_LENGTH_NOT_REACHED
            return err.for_field(field_name, min=min_).to_dict()
        return None

    return validator


def is_not_empty():
    def validator(value, field_name):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return ValidationErrors.EMPTY_STRING.for_field(field_name).to_dict()
        return None

    return validator


def max_length(max_: int, error=None):
    def validator(value, field_name: str):
        if not isinstance(value, str):
            return ValidationErrors.NOT_STRING.for_field(field_name).to_dict()
        if len(value) > max_:
            err = error or ValidationErrors.MAX_LENGTH_REACHED
            return err.for_field(field_name, max=max_).to_dict()
        return None

    return validator
