from datetime import date

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.remaining.serializers import RemainingOutputSerializer
from request.domain import remaining_days


class RemainingView(ReadOnlyModelViewSet):
    serializer_class = RemainingOutputSerializer

    def list(self, request, *args, **kwargs):
        return Response(
            self.serializer_class(
                {"days": remaining_days(request.user, date.today().year)}
            ).data,
            status=status.HTTP_200_OK,
        )
