from django.forms import ModelForm
from django.forms.widgets import DateInput, EmailInput, NumberInput, PasswordInput, TextInput, Textarea, URLInput
from .models import User, Project, Labor, Rental 

from django.contrib.auth.forms import UserCreationForm

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {'username': TextInput(attrs={'class': 'form-control'}),
                    'first_name': TextInput(attrs={'class': 'form-control'}),
                    'last_name': TextInput(attrs={'class': 'form-control'}),
                    'email': EmailInput(attrs={'class': 'form-control'}),
                    'password1': PasswordInput(attrs={'class': 'form-control'}),
                    'password2': PasswordInput(attrs={'class': 'form-control'}),
                    }


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('description', 'date', 'url', 'street', 'city', 'state', 'zip_code', 'reimbursement', 'expiration_date')
        widgets = {'description': Textarea(attrs={'cols':20, 'rows':3, 'class': 'form-control'}),
                    'date': DateInput(attrs={'class': 'form-control'}),
                    'url': URLInput(attrs={'class': 'form-control'}),
                    'street': TextInput(attrs={'class': 'form-control'}),
                    'city': TextInput(attrs={'class': 'form-control'}),
                    'state': TextInput(attrs={'class': 'form-control'}),
                    'zip_code': TextInput(attrs={'class': 'form-control'}),
                    'reimbursement': NumberInput(attrs={'class': 'form-control'}),
                    'expiration_date': DateInput(attrs={'class': 'form-control'}),
                    }
        labels = {'date': 'Date Initiated'}
        

class LaborForm(ModelForm):
    class Meta:
        model = Labor
        fields = ('date', 'total_hours', 'chainsaw_hours', 'small_equip_hours', 'large_equip_hours')
        widgets = {'date': DateInput(attrs={'class': 'datepicker form-control'}),
                    'total_hours': NumberInput(attrs={'class': 'form-control'}),
                    'chainsaw_hours': NumberInput(attrs={'class': 'form-control'}),
                    'small_equip_hours': NumberInput(attrs={'class': 'form-control'}),
                    'large_equip_hours': NumberInput(attrs={'class': 'form-control'}),
                    }
        labels = {'small_equip_hours': 'Small equipment hours', 'large_equip_hours': 'Large equipment hours'}

class RentalForm(ModelForm):
    class Meta:
        model = Rental
        fields = ('equipment', 'cost', 'start_date', 'end_date')
        widgets = {'equipment': TextInput(attrs={'class': 'form-control'}),
                    'cost': NumberInput(attrs={'class': 'form-control'}),
                    'start_date': DateInput(attrs={'class': 'form-control'}),
                    'end_date': DateInput(attrs={'class': 'form-control'}),
                    }