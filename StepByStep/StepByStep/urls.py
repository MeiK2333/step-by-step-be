from django.urls import include, path

from StepByStep.router import router

api_urls = [path("", include("source.urls")), path("", include("user.urls"))]

urlpatterns = [
    path("", include(api_urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
