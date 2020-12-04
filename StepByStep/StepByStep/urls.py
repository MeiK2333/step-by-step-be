from django.urls import include, path
from rest_framework import routers

from user import views
from source import views as source_views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"problems", source_views.ProblemViewSet)
router.register(r"solutions", source_views.SolutionViewSet)
router.register(r"sources", source_views.SourceViewSet)
router.register(r"source_users", source_views.SourceUserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
