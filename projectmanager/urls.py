from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('user/', views.getUser, name='user'),
    path('project/', views.projects, name="projects"),
    path('project/<int:pk>/', views.project_view, name="project"),
    path('project/<int:pk>/tasks/', views.project_tasks, name="tasks"),
    path('project/<int:projpk>/tasks/<int:pk>/', views.project_task_view, name="task"),
    path('project/<int:projpk>/tasks/<int:taskpk>/todo/', views.project_task_todos, name="todos"),
    path('project/<int:projpk>/tasks/<int:taskpk>/todo/<int:pk>/', views.project_task_todo_view, name="todo"),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]