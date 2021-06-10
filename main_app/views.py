from django.shortcuts import render, redirect

from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from django.urls import reverse_lazy

from django.db.models import Sum

# import forms
from .forms import UserCreateForm, ProjectForm, LaborForm, RentalForm, PdfForm

# import models
from .models import User, Project, Labor, Rental, PDF

# AWS imports
import boto3
import uuid

# AWS Constants
S3_BASE_URL = 'https://s3-us-west-2.amazonaws.com/'
BUCKET = 'country-mechanic'

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
        pdf = project.pdf_set.all()
        pdf_form = PdfForm()
        
        # summary costs
        rental_sum = Rental.objects.filter(project_id=project.id).aggregate(Sum('cost'))['cost__sum']
        total_hours_cost = 25 * Labor.objects.filter(project_id=project.id).aggregate(Sum('total_hours'))['total_hours__sum']
        chainsaw_hours_cost = 8 * Labor.objects.filter(project_id=project.id).aggregate(Sum('chainsaw_hours'))['chainsaw_hours__sum']
        small_equipment_hours_cost = 20 * Labor.objects.filter(project_id=project.id).aggregate(Sum('small_equip_hours'))['small_equip_hours__sum']
        large_equipment_hours_cost = 60 * Labor.objects.filter(project_id=project.id).aggregate(Sum('large_equip_hours'))['large_equip_hours__sum']
        total_labor_cost = total_hours_cost + chainsaw_hours_cost + small_equipment_hours_cost + large_equipment_hours_cost
        total_cost = rental_sum + total_labor_cost

        # for status bar
        completion = (total_cost / (project.reimbursement* 2)) * 100

        context = {'user': user, 'project': project, 'rental_sum': rental_sum, 'pdf_form': pdf_form, 'pdf': pdf, "labor_cost": total_labor_cost, 'total_cost': total_cost, 'completion': completion}
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

# ==== PDF ====
def add_pdf(request, pk):
    # photo-file will be the "name" attribute on the <input type="file">
    pdf_file = request.FILES.get('url', None)
    print(pdf_file)
    if pdf_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs pdf file extension too
        key = uuid.uuid4().hex[:6] + \
            pdf_file.name[pdf_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            # adding the ExtraArgs allows the PDF to be opened from an anchor tag
            s3.upload_fileobj(pdf_file, BUCKET, key, ExtraArgs={'ContentType': 'application/pdf'})
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"

            pdf = PDF(url=url, project_id=pk)
            pdf.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('landing')


def delete_pdf(request, pk):
    pdf = PDF.objects.get(pk=pk)
    # delete the row from psql table
    pdf.delete()
    
    # steps below will delete file from AWS S3
    s3 = boto3.client('s3')
    
    # gets the file name from the url created in add_pdf
    key = pdf.url[-10:]
    
    # deletes the file from AWS S3, must be formatted as shown
    s3.delete_object(Bucket=BUCKET, Key=key)

    return redirect('landing')