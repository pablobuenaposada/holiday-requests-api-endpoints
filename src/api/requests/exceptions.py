from rest_framework.exceptions import APIException


class ApiNotEnoughFreeDays(APIException):
    status_code = 409
    default_detail = "Not enough free days"
    default_code = "free_days"


class ApiOverlap(APIException):
    status_code = 409
    default_detail = "This request overlaps with an existing one"
    default_code = "overlap"
