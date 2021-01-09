from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    GENDER = (
        ('Male','Male'),
        ('Female','Female')
        )
    ROLES=(
        ('doctor','Doctor'),
        ('patient','Patient'),
        ('staff','Staff')
    )
    phone = models.CharField(max_length=200,null=True)
    birth_date = models.DateTimeField(null=True)
    gender = models.CharField(max_length=200,null=True,choices=GENDER)
    role=models.CharField(max_length=200,null=True,choices=ROLES)

    # def __str__(self):
    #     return self.UserProfile.name


class Patient(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    medical_history = ArrayField(models.CharField(max_length = 200, null = True), size = 1000, null= True)
    def __str__(self):
        return self.user.username

class Clinic(models.Model):
    name = models.CharField(max_length = 200, null = True)
    rating = models.FloatField(null= True)
    address = models.CharField(max_length = 200, null = True)
    def __str__(self):
        return self.name
 

class Doctor(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete = models.CASCADE,null=True)
    specialization = models.CharField(max_length = 50, null= True)
    rating = models.FloatField(null = True)
    fees =  models.IntegerField(null = True)
    time_slots = ArrayField(models.DateTimeField(null = True), size = 24, null= True)
    description = models.CharField(max_length = 1024, null = True)
    medical_id = models.CharField(max_length = 20, null = True)
    
    def __str__(self):
        return self.user.username


class Staff(models.Model):
    specialization_choices = (
        ('nurse','Nurse'),
        ('lab_specialist','Lab Specialist')
        )
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    specialization = models.CharField(max_length = 20, null= True, choices = specialization_choices)
    def __str__(self):
        return self.user.name

class Appointment(models.Model):
    STATUS = (
			('Pending', 'Pending'),
			('Done', 'Done'),
			('Cancelled', 'Cancelled'),
			)
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    time_slot = models.DateTimeField(null = True)
    review = models.CharField(max_length = 1024)
    prescription = ArrayField(models.CharField(max_length = 70, null= True) , size=10,null= True)
	




class Payment(models.Model):
    key = models.CharField(max_length=250)
    amount = models.IntegerField(null=True)
    appointment = models.ForeignKey(Appointment, on_delete = models.CASCADE)

