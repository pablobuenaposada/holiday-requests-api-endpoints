from django.urls import include, path
from rest_framework import routers

from api.requests.overlaps.views import OverlappingView

router = routers.DefaultRouter()
router.register(r"", OverlappingView, basename="")

urlpatterns = [
    path("", include(router.urls)),
]
