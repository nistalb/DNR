from django.db import models
from datetime import date

from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    description = models.CharField(max_length=500)
    date = models.DateField()
    url = models.URLField(max_length=200, blank=True, help_text='Add the pdf file from DNR describing the project.')
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=11)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

class Labor(models.Model):
    date = models.DateField(default=date.today, help_text='Enter the date the work was performed.')
    total_hours = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, help_text='Enter the hours worked. One and a half hours would be entered as 1.5.')
    chainsaw_hours = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    small_equip_hours = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    large_equip_hours = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    project =  models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.date
    
class Rental(models.Model):
    equipment = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.equipment

    