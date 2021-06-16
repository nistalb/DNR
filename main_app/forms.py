from django.forms import ModelForm
from django.forms.widgets import DateInput, EmailInput, FileInput, NumberInput, PasswordInput, TextInput, Textarea, URLInput
from .models import User, Project, Labor, Rental, PDF 

from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('description', 'date', 'street', 'city', 'state', 'zip_code', 'reimbursement', 'expiration_date')
        labels = {'date': 'Date Initiated'}
        widgets = { 'date': DateInput(attrs={'class': 'datepicker'}),
                    'expiration_date': DateInput(attrs={'class': 'datepicker'}),
                    'description': Textarea(attrs={'rows':3, 'cols':15})
                    }
        

class LaborForm(ModelForm):
    class Meta:
        model = Labor
        fields = ('date', 'total_hours', 'chainsaw_hours', 'small_equip_hours', 'large_equip_hours')
        widgets = {'date': DateInput(attrs={'class': 'datepicker'}),}
        labels = {'small_equip_hours': 'Small equipment hours', 'large_equip_hours': 'Large equipment hours'}

    def clean(self):
        # get the data from the form using the super function
        super(LaborForm, self).clean()

        # extract the total hours, chainsaw hours, small equip hours, and large equip hours
        total_hours = self.cleaned_data.get('total_hours')
        chainsaw_hours = self.cleaned_data.get('chainsaw_hours')
        small_equip_hours = self.cleaned_data.get('small_equip_hours')
        large_equip_hours = self.cleaned_data.get('large_equip_hours')

        # conditions
        if total_hours < chainsaw_hours:
            self._errors['chainsaw_hours'] = self.error_class(['Hours must be less than total hours.'])

        if total_hours < small_equip_hours:
            self._errors['small_equip_hours'] = self.error_class(['Hours must be less than total hours.'])

        if total_hours < large_equip_hours:
            self._errors['large_equip_hours'] = self.error_class(['Hours must be less than total hours.'])

        return self.cleaned_data


class RentalForm(ModelForm):
    class Meta:
        model = Rental
        fields = ('equipment', 'cost', 'start_date', 'end_date')
        widgets = {'equipment': TextInput(attrs={'class': 'form-control'}),
                    'cost': NumberInput(attrs={'class': 'form-control'}),
                    'start_date': DateInput(attrs={'class': 'datepicker form-control'}),
                    'end_date': DateInput(attrs={'class': 'datepicker form-control'}),
                    }

class PdfForm(ModelForm):
    class Meta:
        model = PDF
        fields = ('url',)
        labels = {'url': 'PDF Upload'}
        widgets = {'url': FileInput,}