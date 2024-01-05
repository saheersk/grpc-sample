from django.urls import path

from task_service.api.views import TaskView, TaskDetailView


urlpatterns = [
    path("", TaskView.as_view(), name="all-task"),
    path("<int:pk>/", TaskDetailView.as_view(), name="detail-task"),
]