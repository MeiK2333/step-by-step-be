from django.urls import include, path
from rest_framework import routers

from source import views as source_views
from user import views as user_views

router = routers.DefaultRouter()

router.register(r"problems", source_views.ProblemViewSet)
router.register(r"solutions", source_views.SolutionViewSet)
router.register(r"sources", source_views.SourceViewSet)
router.register(r"source_users", source_views.SourceUserViewSet)

router.register(r"users", user_views.UserViewSet)
# router.register(r"groups", user_views.GroupViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(r"login/", user_views.LoginAPIView.as_view()),
    path(r"logout/", user_views.LogoutAPIView.as_view()),
]
