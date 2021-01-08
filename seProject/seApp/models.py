from django.db import models
from django.contrib.postgres.fields import ArrayField

class User(models.Model):
    GENDER = (
        ('Male','Male'),
        ('Female','Female')
        )
    name = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    data_created = models.DateTimeField(auto_now_add=True,null=True)
    birth_date = models.DateTimeField(null=True)
    gender = models.CharField(max_length=200,null=True,choices=GENDER)
    def __str__(self):
        return self.name


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medical_history = ArrayField(models.CharField(max_length = 200, null = True), size = 1000, null= True)
    def __str__(self):
        return self.user.name

class Clinic(models.Model):
    name = models.CharField(max_length = 200, null = True)
    rating = models.FloatField(null= True)
    address = models.CharField(max_length = 200, null = True)
    def __str__(self):
        return self.name
 

class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete = models.CASCADE)
    specialization = models.CharField(max_length = 50, null= True)
    rating = models.FloatField(null = True)
    fees =  models.IntegerField(null = True)
    time_slots = ArrayField(models.DateTimeField(null = True), size = 24, null= True)
    description = models.CharField(max_length = 1024)
    
    def __str__(self):
        return self.user.name


class Staff(models.Model):
    specialization_choices = (
        ('nurse','Nurse'),
        ('lab_specialist','Lab Specialist')
        )
    user = models.ForeignKey(User, on_delete = models.CASCADE)
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

