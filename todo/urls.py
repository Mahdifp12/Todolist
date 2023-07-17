from django.urls import path
from . import views

urlpatterns = [
    path('', views.TodoListView.as_view(), name="todo-list"),
    path('add-todo/', views.AddTodo.as_view(), name="add-todo-page"),
    path('todo/<slug:slug>', views.TodoDetailView.as_view(), name="todo-detail-page"),
    path('todo/delete/<slug:slug>', views.TodoCompleted.as_view(), name="todo-completed-page"),
]