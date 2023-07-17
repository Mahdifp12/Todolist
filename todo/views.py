from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django.views import View
from django.contrib import messages
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


class TodoDetailView(DetailView):
    model = ItemTodo
    template_name = "todo/todo_detail_page.html"
    context_object_name = 'todo'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.user != self.request.user:
            raise Http404("شما مجاز به دیدن این صفحه نیستید.")
        return obj


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


class TodoCompleted(DeleteView):
    model = ItemTodo
    template_name = "todo/todo_completed_page.html"
    context_object_name = 'todo'
    success_url = reverse_lazy('todo-list')

    def form_valid(self, form):
        todo = self.get_object()
        todo.completed = True
        todo.save()
        messages.success(self.request, "تو دو شما با موفقیت به پایان رسید ...")
        return super(TodoCompleted, self).form_valid(form)
