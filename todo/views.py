from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from helpers.views import create_or_update_todo
from .models import Todo

from todo.forms import TodoForm


def get_showing_todos(request, todos):
    if request.GET and request.GET.get('filter'):
        if request.GET.get('filter') == 'complete':
            return todos.filter(is_completed=True)
        if request.GET.get('filter') == 'incomplete':
            return todos.filter(is_completed=False)
    return todos


@login_required
def index(request):
    todos = Todo.objects.filter(owner=request.user)
    completed_count = todos.filter(is_completed=True).count()
    incompleted_count = todos.filter(is_completed=False).count()
    all_count = todos.count()

    context = {'todos': get_showing_todos(request, todos),
               'completed_count': completed_count,
               'incompleted_count': incompleted_count,
               'all_count': all_count}
    return render(request, 'todo/index.html', context=context)

@login_required
def create_todo(request):
    form = TodoForm()
    context = {'form': form}

    if request.method == 'POST':
        todo = create_or_update_todo(request, param='create')
        return HttpResponseRedirect(reverse('todo', kwargs={'id': todo.pk}))

    return render(request, 'todo/create_todo.html', context=context)

@login_required
def todo_detail(request, id):
    todo = get_object_or_404(Todo, pk=id)
    if request.user == todo.owner:
        context = {'todo': todo}
        return render(request, 'todo/todo_detail.html', context=context)
    return redirect('home')

@login_required
def todo_delete(request, id):
    todo = get_object_or_404(Todo, pk=id)
    context = {'todo': todo}
    if request.method == 'POST':
        if todo.owner == request.user:
            todo.delete()
            messages.add_message(request, messages.SUCCESS, "Todo deleted successfully")
            return HttpResponseRedirect(reverse('home'))
        return render(request, 'todo/todo_delete.html', context=context)
    return render(request, 'todo/todo_delete.html', context=context)

@login_required
def todo_edit(request, id):
    todo = get_object_or_404(Todo, pk=id)
    if request.user == todo.owner:
        form = TodoForm(instance=todo)
        context = {'todo': todo, 'form': form}
        if request.method == 'POST':
            create_or_update_todo(request, todo=todo)
            return HttpResponseRedirect(reverse('todo', kwargs={'id': todo.pk}))
        return render(request, 'todo/todo_edit.html', context=context)
    return redirect('home')