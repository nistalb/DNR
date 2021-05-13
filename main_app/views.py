from django.shortcuts import render, redirect
from django.contrib.auth import login

# import forms
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm, ProjectForm

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
    return render(request, 'register.html', context)

# ==== LANDING ====
def landing(request):
    
    user = User.objects.get(id=request.user.id)
    project = Project.objects.get(user_id=request.user.id)
    context = {'user': user, 'project': project}
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

    project_form = ProjectForm(instance=project)
    context = {'project_form': project_form, 'project': project}
    return render(request, 'project/edit.html', context)
