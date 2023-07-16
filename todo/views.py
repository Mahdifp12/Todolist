from django.shortcuts import render
from django.views.generic import ListView
from .models import ItemTodo


# Create your views here.

class TodoListView(ListView):
    model = ItemTodo
    template_name = "todo/todo_list.html"
    context_object_name = 'todos'
