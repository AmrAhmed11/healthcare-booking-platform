from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import  UserCreationForm
from django import forms
from django.db import transaction

class PrescriptionForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ('prescription',)

class DateInput(forms.DateInput):
    input_type='Date'

class CreatePatientForm (UserCreationForm):
    class Meta:
        model=UserProfile
        fields=['username','email','password1','password2','gender','phone','birth_date']
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'birth_date':DateInput()
        }
    def save(self):
        user = super().save(commit=False)
        user.role = 'Patient'
        user.save()
        patient = Patient.objects.create(user=user)
        return user


class CreateDoctorForm (UserCreationForm):
    class Meta:
        model=UserProfile
        fields=['username','email','password1','password2','gender','phone','birth_date']
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'birth_date':DateInput()
        }
    def save(self):
        user = super().save(commit=False)
        user.role = 'Doctor'
        user.save()
        doctor = Doctor.objects.create(user=user)
        return user

        
class CreateStaffForm (UserCreationForm):
    class Meta:
        model=UserProfile
        fields=['username','email','password1','password2','gender','phone','birth_date']
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'birth_date':DateInput()
        }
    def save(self):
        user = super().save(commit=False)
        user.role = 'Staff'
        user.save()
        staff = Staff.objects.create(user=user)
        return user


