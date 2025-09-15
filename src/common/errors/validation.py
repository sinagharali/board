class ValidationErrorInstance:
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message

    def to_dict(self):
        return {"code": self.code, "message": self.message}


class ValidationErrorObject:
    def __init__(self, code: str, message: str):
        self.code = code
        self.message_template = message

    def for_field(self, field_name: str, **kwargs):
        # Prepare template dict with field + any extra info
        template_vars = {"field": field_name, **kwargs}
        message = self.message_template.format(**template_vars)
        return ValidationErrorInstance(self.code, message)

    def to_dict(self):
        return {"code": self.code, "message": self.message_template}  # fallback


class ValidationErrors:
    EMAIL_INVALID = ValidationErrorObject(
        code="invalid_email",
        message="{field} must contain @ and a domain",
    )
    PASSWORD_WEAK = ValidationErrorObject(
        code="password_weak",
        message="{field} is weak",
    )
    NOT_STRING = ValidationErrorObject(
        code="not_a_string",
        message="{field} must be a string",
    )
    MAX_LENGTH_REACHED = ValidationErrorObject(
        code="max_length_reached",
        message="{field} has reached maximum {max} length",
    )
    NOT_IN_RANGE = ValidationErrorObject(
        code="not_in_range",
        message="{field} must be in range of {min} to {max}",
    )
    EMPTY_STRING = ValidationErrorObject(
        code="empty_string",
        message="{field} should not be empty",
    )
    MIN_LENGTH_NOT_REACHED = ValidationErrorObject(
        code="min_length_not_reached",
        message="{field} must have at least {min} charecter",
    )
