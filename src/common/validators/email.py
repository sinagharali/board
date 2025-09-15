import re

from common.errors.validation import ValidationErrors

MAX_EMAIL_LENGTH = 254


MAX_EMAIL_LENGTH = 254


def validate_email(error_max_length=None, error_invalid=None):
    def validator(value: str, field_name: str):
        errors = []

        if not isinstance(value, str):
            return ValidationErrors.NOT_STRING.for_field(field_name).to_dict()

        # Max length check
        if len(value) > MAX_EMAIL_LENGTH:
            err = error_max_length or ValidationErrors.MAX_LENGTH_REACHED
            errors.append(err.for_field(field_name).to_dict())

        # Basic email pattern check
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            err = error_invalid or ValidationErrors.EMAIL_INVALID
            errors.append(err.for_field(field_name).to_dict())

        if errors:
            return errors
        return None

    return validator
