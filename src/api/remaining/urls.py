from django.urls import include, path
from rest_framework import routers

from api.remaining.views import RemainingView

router = routers.DefaultRouter()
router.register(r"", RemainingView, basename="")

urlpatterns = [
    path("", include(router.urls)),
]
