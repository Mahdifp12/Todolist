from django.urls import path
from . import views

urlpatterns = [
    path('', views.TodoListView.as_view(), name="todo-list"),
]