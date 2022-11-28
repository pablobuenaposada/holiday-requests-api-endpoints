from django.urls import include, path
from rest_framework import routers

from api.requests.views import RequestView

router = routers.DefaultRouter()
router.register(r"", RequestView, basename="")

urlpatterns = [
    path("overlaps/", include("api.requests.overlaps.urls")),
    path("", include(router.urls)),
]
