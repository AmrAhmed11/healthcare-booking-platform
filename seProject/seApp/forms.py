from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import  UserCreationForm
from django import forms
from django.db import transaction


class DateInput(forms.DateInput):
    input_type='Date'

class CreateUserForm (UserCreationForm):
    class Meta:
        model=UserProfile
        fields=['first_name','last_name','username','email','password1','password2','gender','phone','birth_date','role']
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'birth_date':DateInput(),
            'role': forms.Select(attrs={'class': 'form-control'})
        }
    def save(self):
        user = super().save(commit=False)        
        user.save()
        if(user.role == 'patient'):
            patient = Patient.objects.create(user=user)
        elif(user.role == 'doctor'):
            doctor = Doctor.objects.create(user=user)
        elif(user.role == 'staff'):
            staff = Staff.objects.create(user=user)
        return user

class ReviewForm(ModelForm):
    class Meta:
        model = Appointment 
        fields = ['review',]


class chooseAppointmentForm(ModelForm):
    class Meta:
        model = Doctor
        fields =['time_slots',]