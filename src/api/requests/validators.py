from django.core.exceptions import ValidationError


def dates_validator(value):
    if value["vacation_start_date"] >= value["vacation_end_date"]:
        raise ValidationError(
            "vacation_start_date should be earlier than vacation_end_date"
        )
