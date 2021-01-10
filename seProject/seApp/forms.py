from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import  UserCreationForm
from django import forms
from django.contrib.auth.models import  User


class CreateUserForm (UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2',]

class ReviewForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ('review',)

class chooseAppointmentForm(ModelForm):
    class Meta:
        model = Doctor
        fields =['time_slots',]