import string

from common.errors.validation import ValidationErrors

MAX_PASSWORD_LIMIT = 64
MIN_PASSWORD_LIMIT = 8
MIN_SCORE = 6


def validate_password(error_not_in_range=None, error_weak=None):
    def validator(value: str, field_name: str):
        errors = []

        if not isinstance(value, str):
            return ValidationErrors.NOT_STRING.for_field(field_name).to_dict()

        # Length check
        if not (MIN_PASSWORD_LIMIT <= len(value) <= MAX_PASSWORD_LIMIT):
            err = error_not_in_range or ValidationErrors.NOT_IN_RANGE
            errors.append(
                err.for_field(
                    field_name,
                    min=MIN_PASSWORD_LIMIT,
                    max=MAX_PASSWORD_LIMIT,
                ).to_dict(),
            )

        # Score calculation
        upper_case = any(c.isupper() for c in value)
        lower_case = any(c.islower() for c in value)
        special = any(c in string.punctuation for c in value)
        digits = any(c.isdigit() for c in value)

        score = sum([upper_case, lower_case, special, digits]) + (len(value) % 4)

        if score < MIN_SCORE:
            err = error_weak or ValidationErrors.PASSWORD_WEAK
            errors.append(err.for_field(field_name).to_dict())

        if errors:
            return errors
        return None

    return validator
