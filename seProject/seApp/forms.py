from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import  UserCreationForm
from django import forms
from django.contrib.auth.models import  User

class PrescriptionForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ('prescription',)

class CreateUserForm (UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']