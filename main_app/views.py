from django.shortcuts import render, redirect
from django.contrib.auth import login

# import forms
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm, ProjectForm, LaborForm

# import models
from .models import User, Project, Labor, Rental

# Create your views here.

# ====  HOME  ====
def home(request):
    return render(request, 'home.html')

# ==== REGISTER ====
def register(request):
    if request.method =='POST':
        registration_form = NewUserForm(request.POST)
        if registration_form.is_valid:
            user = registration_form.save() 
            login(request, user)
            return redirect('project_create')

    registration_form = NewUserForm()
    auth_form = AuthenticationForm()
    context = {'registration_form': registration_form, 'auth_form': auth_form}
    return render(request, 'register/register.html', context)

def register_edit(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.username = request.POST['username']
        user.save()  
        return redirect('landing')

    user_form = NewUserForm(instance=user)
    context = {'user_form': user_form}
    return render(request, 'register/edit.html', context)

# ==== LANDING ====
def landing(request):
    user = User.objects.get(id=request.user.id)
    project = Project.objects.get(user_id=request.user.id)
    labor = Labor.objects.filter(project_id=project.id).order_by('date')
    print(labor)
    print('here')
    labor_form = LaborForm()
    context = {'user': user, 'project': project, 'labor_form': labor_form, 'labor': labor}
    return render(request, 'landing.html', context)

# ==== PROJECT ====
def project_create(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        if project_form.is_valid:
            project = project_form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('landing')

    project_form = ProjectForm()
    context = {'project_form': project_form}
    return render(request, 'project/create.html', context)

def project_edit(request):
    project = Project.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        if project_form.is_valid:
            project_form.save()
            return redirect('landing')

    project_form = ProjectForm(instance=project)
    context = {'project_form': project_form, 'project': project}
    return render(request, 'project/edit.html', context)

# ==== LABOR ====
def labor_create(request):
    # New Labor form is in landing route
    project = Project.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        labor_form = LaborForm(request.POST)
        if labor_form.is_valid:
            labor = labor_form.save(commit=False)
            labor.project = project
            labor.save()
            return redirect('landing')

def labor_edit(request, labor_id):
    labor = Labor.objects.get(id=labor_id)
    if request.method == 'POST':
        labor_form = LaborForm(request.POST, instance=labor)
        if labor_form.is_valid:
            labor_form.save()
            return redirect('landing')

    labor_form = LaborForm(instance=labor)
    context = {'labor_form': labor_form, 'labor': labor}
    return render(request, 'labor/edit.html', context)