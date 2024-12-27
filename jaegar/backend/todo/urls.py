from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet, GenerateRandomNumberView

router = DefaultRouter()
router.register("todos", TodoViewSet, basename="todo")

urlpatterns = [
    path("", include(router.urls)),
    path("tasks/random/", GenerateRandomNumberView.as_view(), name="generate-random-number"),
    path("tasks/random/<str:task_id>/", GenerateRandomNumberView.as_view(), name="task-status"),
]
