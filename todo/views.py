from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TodoForm
from .models import Todo, Status
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
# Create your views here.


def home(request):
    return render(request, 'todo/home.html')


def signupUser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if(password1 == password2):
            try:
                user = User.objects.create_user(username, password=password1)
                user.save()
                login(request, user)
                return redirect('currentTodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'error': 'That username already been taken! Please choose a new username.', 'form': UserCreationForm()})
            # except:
            #     return render(request, 'todo/signupuser.html', {'error': 'Unknown error occurred!','form': UserCreationForm()})

        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords did not match'})


def loginUser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username and Password did not match!'})
        else:
            login(request, user)
            return redirect('currentTodos')


@login_required
def logoutUser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')


@login_required
def currentTodos(request):
    todos = Todo.objects.filter(user=request.user, dateCompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})


@login_required
def createTodo(request):
    if request.method == "GET":
        return render(request, 'todo/createtodo.html', {'form': TodoForm})
    else:
        try:
            form = TodoForm(request.POST)
            Todo = form.save(commit=False)
            Todo.user = request.user
            Todo.save()
            return redirect('currentTodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm, 'error': 'Bad data passed in! Try again.'})


@login_required
def viewTodo(request, todoPK):
    todo = get_object_or_404(Todo, pk=todoPK, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            status = Status.objects.get(pk=request.POST['status'])
            # print(status.name)
            if status.name == "Completed":
                todo.dateCompleted = timezone.now()
                form = TodoForm(request.POST, instance=todo)
            if status.name == "In progress":
                todo.dateCompleted = None
                form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currentTodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Bad Info!'})


@login_required
def deleteTodo(request, todoPK):
    todo = get_object_or_404(Todo, pk=todoPK, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currentTodos')


@login_required
def completedTodos(request):
    todos = Todo.objects.filter(
        user=request.user, dateCompleted__isnull=False).order_by('-dateCompleted')
    return render(request, 'todo/completedtodos.html', {'todos': todos})

class TodoCreateView(CreateView):
    model = Todo
    fields = ('title', 'note', 'status', 'materiality', 'isActive')
