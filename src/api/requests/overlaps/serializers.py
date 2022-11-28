from api.requests.serializers import RequestOutputSerializer
from request.models import Request


class OverlapOutputSerializer(RequestOutputSerializer):
    overlaps = RequestOutputSerializer(many=True)

    class Meta:
        model = Request
        fields = ["id", "overlaps", "vacation_start_date", "vacation_end_date"]
