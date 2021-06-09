from django.shortcuts import render, redirect

from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from django.urls import reverse_lazy

from django.db.models import Sum

# import forms
from .forms import UserCreateForm, ProjectForm, LaborForm, RentalForm

# import models
from .models import User, Project, Labor, Rental

# Create your views here.

# ====  HOME  ====
class HomeView(TemplateView):
    template_name = 'home.html'

# ==== REGISTER ====
class Register(CreateView):
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'register/register.html'

class RegisterUdpateView(UpdateView):
    model = User
    # specify the fields that can be updated
    fields = ['username', 'first_name', 'last_name', 'email']
    success_url = reverse_lazy('landing')
    template_name = 'register/edit.html'

# ==== LANDING ====
def landing(request):
    if request.user.id in Project.objects.values_list('owner_id', flat=True):
        user = User.objects.get(id=request.user.id)
        project = Project.objects.get(owner_id=request.user.id)
        rental_sum = Rental.objects.filter(project_id=project.id).aggregate(Sum('cost'))['cost__sum']
        context = {'user': user, 'project': project, 'rental_sum': rental_sum}
        return render(request, 'landing.html', context)
    else:
        return redirect('project_create')

# ==== PROJECT ==== 
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('landing')
    # uses default template at main_app/project_form.html

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner  = self.request.user
        self.object.save()
        return super().form_valid(form)

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('landing')
    # uses default template at main_app/project_form.html

# ==== LABOR ====
def labor_create(request):
    project = Project.objects.get(owner_id=request.user.id)
    labor = Labor.objects.filter(project_id=project.id)
    if request.method == 'POST':
        labor_form = LaborForm(request.POST)
        if labor_form.is_valid:
            labor = labor_form.save(commit=False)
            labor.project = project
            labor.save()
            return redirect('labor_create')

    labor_form = LaborForm()
    context = {'labor_form': labor_form, 'labor': labor}
    return render(request, 'labor/create.html', context)

class LaborUpdateView(UpdateView):
    model = Labor
    form_class = LaborForm
    success_url = reverse_lazy('labor_create')
    template_name = 'labor/edit.html'

class LaborDeleteView(DeleteView):
    model = Labor
    success_url = reverse_lazy('labor_create')
    # uses default template at main_app/labor_confirm_delete.html

# ==== RENTAL ====
def rental_create(request):
    project = Project.objects.get(owner_id=request.user.id)
    rental = Rental.objects.filter(project_id=project.id)
    if request.method == 'POST':
        rental_form = RentalForm(request.POST)
        if rental_form.is_valid:
            rental = rental_form.save(commit=False)
            rental.project = project
            rental.save()
            return redirect('rental_create')

    rental_form = RentalForm()
    context = {'rental_form': rental_form, 'rental': rental}
    return render(request, 'rental/create.html', context)

class RentalUpdateView(UpdateView):
    model = Rental
    form_class = RentalForm
    success_url = reverse_lazy('rental_create')
    template_name = 'rental/edit.html'

class RentalDeleteView(DeleteView):
    model = Rental
    success_url = reverse_lazy('rental_create')
    # uses default template at main_app/rental_confirm_delete.html