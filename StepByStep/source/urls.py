from django.urls import include, path
from source import views
from StepByStep.router import router

router.register(r"problems", views.ProblemViewSet)
router.register(r"solutions", views.SolutionViewSet)
router.register(r"sources", views.SourceViewSet)
router.register(r"source_users", views.SourceUserViewSet)

urlpatterns = [path("", include(router.urls))]
