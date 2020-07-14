from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todo/home.html')


def signup_user(request):

    context = {
        'form': UserCreationForm(),
    }

    if request.method == 'GET':
        return render(request, 'auth/signup.html', context)
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('todo:current_todo')
            except IntegrityError:
                context['error'] = "User name already in Taken"
                return render(request, 'auth/signup.html', context)

        else:
            # password doesn't match
            context['error'] = "Paswords doesn't match"
            print("Password doesn't match")
            return render(request, 'auth/signup.html', context)


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('todo:home_todo')


def login_user(request):
    context = {
        'form': AuthenticationForm(),
    }

    if request.method == 'GET':
        return render(request, 'auth/login.html', context)
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            context['error'] = "Wrong Username or Password"
            return render(request, 'auth/login.html', context)
        else:
            login(request, user)
            return redirect('todo:current_todo')


@login_required
def current_todo(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    context = {
        "list": todos
    }
    return render(request, 'todo/current_todo.html', context)


@login_required
def completed_todo(request):
    todos = Todo.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    context = {
        "list": todos
    }
    return render(request, 'todo/completed_todo.html', context)


@login_required
def detail_todo(request, todo_pk):
    todo = get_object_or_404(Todo, id=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        context = {
            'detail': todo,
            'form': form,
            'error': '',
        }
        return render(request, 'todo/detail.html', context)
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('todo:current_todo')
        except ValueError:
            context['error'] = "Bad data passed in. Try Again"
            return render(request, 'todo/detail.html', context)


@login_required
def complete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('todo:current_todo')


@login_required
def delete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo:current_todo')


@login_required
def create_todo(request):
    context = {
        'form': TodoForm(),
        'error': ''
    }
    if request.method == 'GET':
        return render(request, 'todo/create_todo.html', context)
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('todo:current_todo')
        except ValueError:
            context['error'] = "Bad data passed in. Try Again"
            return render(request, 'todo/create_todo.html', context)
