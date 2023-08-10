
from django import forms
from .models import *
from django.db.models import fields
from django.contrib.auth.forms import UserCreationForm

class CreateEmployee(UserCreationForm):
    class Meta:
        model = Employee
        fields = ('name','username', 'empid','designation', 'department','phone_number', 'email','login_counter','logout_counter',  'password1', 'password2')

class ChangeEmployeePermission(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ("name","permission",)

from .models import Employee

class IndividualEmpAttendance(forms.ModelForm):
    class Meta:
        model = IndividualEmployeeAttendance
        fields = ("employee", "start_date","end_date")