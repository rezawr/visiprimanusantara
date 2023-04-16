from django.urls import include, path

app_name = "api"
urlpatterns = [
    path("v1.0/", include("visi.api.v1_0.urls", namespace="v1.0")),
]
