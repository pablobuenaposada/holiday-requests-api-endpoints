from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.requests.overlaps.serializers import OverlapOutputSerializer
from api.requests.permissions import ManagerPermission
from request.constants import STATUS_PENDING
from request.models import Request


class OverlappingView(mixins.ListModelMixin, GenericViewSet):
    serializer_class = OverlapOutputSerializer
    queryset = Request.objects.filter(status=STATUS_PENDING)
    permission_classes = [IsAuthenticated, ManagerPermission]
