from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from . forms import CreateUserForm, LoginForm, TaskForm
from . models import Tasks

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'dolist/index.html')

def login(request):
    form = LoginForm()
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)

            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')

    context = {'loginForm': form}

    return render(request, 'dolist/login.html', context)

def register(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'registerForm': form}

    return render(request, 'dolist/register.html', context)

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    if request.user.is_authenticated:
        tasks = Tasks.objects.all()
    else:
        tasks = []
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    
    context = {'tasks': tasks, 'taskForm': form}

    return render(request, 'dolist/dashboard.html', context=context)

def edit_task(request, task_id):
    task = get_object_or_404(Tasks,id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)

    context = {'editForm': form}

    return render(request, 'dolist/edit_task.html', context=context)

def delete_task(request, task_id):
    task  = get_object_or_404(Tasks, id=task_id)

    task.delete()

    return redirect('dashboard')



