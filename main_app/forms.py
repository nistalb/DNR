from django.forms import ModelForm
from .models import User, Project, Labor, Rental 

from django.contrib.auth.forms import UserCreationForm

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('description', 'date', 'url', 'street', 'city', 'state', 'zip_code')

class LaborForm(ModelForm):
    class Meta:
        model = Labor
        fields = ('date', 'total_hours', 'chainsaw_hours', 'small_equip_hours', 'large_equip_hours')