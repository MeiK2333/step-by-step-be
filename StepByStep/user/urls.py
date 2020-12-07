from django.urls import include, path
from source import views as source_views
from StepByStep.router import router

from user import views

router.register(r"users", views.UserViewSet)
# router.register(r"groups", views.GroupViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(r"login", views.LoginAPIView.as_view()),
    path(r"logout", views.LogoutAPIView.as_view()),
]
