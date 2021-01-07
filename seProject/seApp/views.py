from django.shortcuts import render, redirect
from .forms import PrescriptionForm
from django.utils.dateparse import parse_datetime
from pytz import timezone
import pytz
from django.http import HttpResponse
from .models import *
from .forms import CreateUserForm
from django.forms import inlineformset_factory
from django.contrib.auth.forms import  UserCreationForm
from django.contrib import messages
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.decorators import login_required


def loginpage (request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method=='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,'Username or password is not correct')
                return render(request, 'seApp/login.html')
    return render(request, 'seApp/login.html')


def logoutuser (request):
    logout(request)
    return redirect ('loginpage')


def register (request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form =CreateUserForm()
        if request.method == 'POST':
            form =CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Account is created successfully')
                return redirect('loginpage')
    context ={ 'form' : form }
    return render(request, 'seApp/register.html',context)



def index(request):
    return render(request, 'seApp/index.html')


def appointmentManager(request):
    doctor = Doctor.objects.get(id=1)
    app_list = doctor.appointment_set.all()
    context = {'app_list': app_list}
    return render(request, 'seApp/appointmentManager.html', context)

def appointment(request, app_id):
    form = PrescriptionForm()
    app = Appointment.objects.get(id=app_id)
    form = PrescriptionForm(instance=app)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=app)        
        if form.is_valid():
            form.save()

    context = {'app': app, 'doctor': app.doctor, 'patient': app.patient, 'form': form}
    return render(request, 'seApp/appointment.html', context)


def servicesManager(request):
    doctor = Doctor.objects.get(id=1)
    services_list = {'fees':doctor.fees, 'timeslots':doctor.time_slots }
    context = {'services_list': services_list}
    return render(request, 'seApp/servicesManager.html', context)

def changeFeeDoctor(request):
    fee = request.POST['fees']
    doctor = Doctor.objects.get(id=1)
    doctor.fees = fee
    doctor.save()
    return redirect('seApp:servicesManager')

def deleteTimeslotDoctor(request):
    timeslot = request.POST['timeslot']
    print(timeslot)
    doctor = Doctor.objects.get(id=1)
    timeslotParsed = parse_datetime(timeslot) 
    

    doctor.time_slots.remove(timeslotParsed)
    doctor.save()
    return redirect('seApp:servicesManager')

def addTimeslotDoctor(request):
    timeslot = request.POST['timeslot']
    print(timeslot)
    doctor = Doctor.objects.get(id=1)
    doctor.time_slots.append(timeslot)
    doctor.save()
    return redirect('seApp:servicesManager')


def staffManager(request):
    staff_list = [{'id':0, 'name':'John', 'details': 'nurse'}, {'id':1, 'name':'John', 'details': 'nurse'},{'id':2, 'name':'John', 'details': 'nurse'},{'id':3, 'name':'John', 'details': 'nurse'}]
    context = {'staff_list': staff_list}
    return render(request, 'seApp/staffManager.html', context)


def browse(request):
    doctors = Doctor.objects.all()
    context = {'doctors':doctors}
    return render(request,'seApp/browse.html',context)