from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='register/login.html'), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('register/<pk>/edit', views.RegisterUdpateView.as_view(), name='register_edit'),
    path('landing/', views.landing, name='landing'),
    path('project/create', views.ProjectCreateView.as_view(), name='project_create'),
    path('project/<pk>/edit', views.ProjectUpdateView.as_view(), name='project_edit'),
    path('project/<pk>/add_pdf', views.add_pdf, name='add_pdf'),
    path('project/<pk>/delete_pdf', views.delete_pdf, name='delete_pdf'),
    path('labor/create', views.labor_create, name='labor_create'),
    path('labor/<pk>/edit', views.LaborUpdateView.as_view(), name='labor_edit'),
    path('labor/<pk>/delete', views.LaborDeleteView.as_view(), name='labor_delete'),
    path('rental/create', views.rental_create, name='rental_create'),
    path('rental/<pk>/edit', views.RentalUpdateView.as_view(), name='rental_edit'),
    path('rental/<pk>/delete', views.RentalDeleteView.as_view(), name='rental_delete'),
]