from rest_framework import serializers

from api.requests.validators import dates_validator
from request.constants import STATUS_APPROVED, STATUS_REJECTED
from request.models import Request


class RequestOutputSerializer(serializers.ModelSerializer):
    request_created_at = serializers.DateTimeField(source="created")

    class Meta:
        model = Request
        fields = [
            "id",
            "author",
            "status",
            "resolved_by",
            "request_created_at",
            "vacation_start_date",
            "vacation_end_date",
        ]


class RequestInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ["vacation_start_date", "vacation_end_date"]
        validators = [dates_validator]


class RequestUpdateInputSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=[(STATUS_APPROVED, "Approved"), (STATUS_REJECTED, "Rejected")]
    )

    class Meta:
        model = Request
        fields = ["status"]
