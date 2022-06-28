from django.shortcuts import render
from django.contrib import messages
from todo.models import Todo


def handle_not_found(request, exception):
    return render(request, 'not_found.html')


def handle_server_error(request):
    return render(request, 'server_error.html')


def create_or_update_todo(request, param=None, todo=None):
    if param == 'create':
        todo = Todo()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_completed = request.POST.get('is_completed', False)
        todo.title = title
        todo.description = description
        todo.is_completed = True if is_completed == "on" else False
        todo.owner = request.user
        todo.save()
        if param == 'create':
            messages.add_message(request, messages.SUCCESS, "Todo created successfully")
        else:
            messages.add_message(request,messages.SUCCESS, "Todo updated successfully")
        return todo
