from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views import View
from .models import ItemTodo
from .forms import AddTodoForm


# Create your views here.

class TodoListView(ListView):
    model = ItemTodo
    template_name = "todo/todo_list.html"
    context_object_name = 'todos'

    def get_queryset(self):
        query = super(TodoListView, self).get_queryset()
        query = query.filter(user__id__iexact=self.request.user.id)
        return query


class AddTodo(View):
    def get(self, request: HttpRequest):
        add_todo_form = AddTodoForm()
        context = {
            "form": add_todo_form,
        }
        return render(request, 'todo/add_todo_page.html', context)

    def post(self, request: HttpRequest):
        add_todo_form = AddTodoForm(request.POST)
        if add_todo_form.is_valid():
            title = add_todo_form.cleaned_data.get("title")
            description = add_todo_form.cleaned_data.get("description")
            user = request.user.id
            new_todo = ItemTodo(
                title=title,
                description=description,
                user_id=user
            )

            new_todo.save()

            return redirect(reverse("todo-list"))
