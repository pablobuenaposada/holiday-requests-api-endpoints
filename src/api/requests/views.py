from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.requests.exceptions import ApiNotEnoughFreeDays, ApiOverlap
from api.requests.permissions import ManagerPermission
from api.requests.serializers import (RequestInputSerializer,
                                      RequestOutputSerializer,
                                      RequestUpdateInputSerializer)
from request.constants import WORKER_TYPE
from request.exceptions import NotEnoughFreeDays, Overlap
from request.models import Request


class RequestView(mixins.ListModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = RequestOutputSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "author"]

    def get_queryset(self):
        if self.request.user.type == WORKER_TYPE:
            return Request.objects.filter(author=self.request.user)
        return Request.objects.all()

    def get_permissions(self):
        if self.request.method == "PATCH":
            self.permission_classes = [ManagerPermission]

        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        input_serializer = RequestInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        try:
            request = Request.objects.create(
                **input_serializer.validated_data, author=request.user
            )
        except NotEnoughFreeDays:
            raise ApiNotEnoughFreeDays()
        except Overlap:
            raise ApiOverlap()

        return Response(
            self.serializer_class(request).data, status=status.HTTP_201_CREATED
        )

    def partial_update(self, request, *args, **kwargs):
        input_serializer = RequestUpdateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        request = Request.objects.get(id=kwargs["pk"])
        request.status = input_serializer.validated_data["status"]
        request.resolved_by = self.request.user
        request.save(update_fields=["resolved_by", "status"])

        return Response(self.serializer_class(request).data)
