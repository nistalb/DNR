from django.forms import ModelForm
from django.forms.widgets import DateInput, EmailInput, FileInput, NumberInput, PasswordInput, TextInput, Textarea, URLInput
from .models import User, Project, Labor, Rental 

from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('description', 'date', 'url', 'street', 'city', 'state', 'zip_code', 'reimbursement', 'expiration_date')
        labels = {'date': 'Date Initiated', 'url': 'PDF Upload'}
        widgets = {'url': FileInput}
        

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
                    'start_date': DateInput(attrs={'class': 'datepicker form-control'}),
                    'end_date': DateInput(attrs={'class': 'datepicker form-control'}),
                    }