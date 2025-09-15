# common/validators/runner.py
from typing import Callable


def run_validators(value, validators: list[Callable], field_name: str):
    errors = []

    # Only skip validators if the value is exactly None and the field allows None
    for validator in validators:
        # Run validator even if value is empty string, but skip if it's None
        if value is None:
            continue

        err = validator(value, field_name)
        if err:
            if isinstance(err, list):
                errors.extend(err)
            else:
                errors.append(err)

    return errors
