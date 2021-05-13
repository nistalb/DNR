from django.urls import path, include
from . import views

urlpatterns = [
path('', views.home, name='home'),
path('accounts/', include('django.contrib.auth.urls')),
path('register/', views.register, name='register'),
path('register/edit', views.register_edit, name='register_edit'),
path('landing/', views.landing, name='landing'),
path('project/create', views.project_create, name='project_create'),
path('project/edit', views.project_edit, name='project_edit'),
path('labor/create', views.labor_create, name='labor_create'),
]