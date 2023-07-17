from django.urls import path
from . import views

urlpatterns = [
    path('', views.TodoListView.as_view(), name="todo-list"),
    path('add-todo/', views.AddTodo.as_view(), name="add-todo-page"),
]