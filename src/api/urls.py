from django.urls import include, path

urlpatterns = [
    path("requests/", include("api.requests.urls")),
    path("remaining/", include("api.remaining.urls")),
]
