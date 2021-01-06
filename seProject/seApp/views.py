from django.shortcuts import render,redirect
from .models import Doctor
from django.utils.dateparse import parse_datetime
from pytz import timezone
import pytz

# Create your views here.
def index(request):
    
    return render(request, 'seApp/index.html')


def appointmentManager(request):
    app_list = [{'id':0, 'date':'1/1/2022', 'state': 'Pending'}, {'id':1, 'date':'1/2/2022', 'state': 'Pending'}, {'id':2, 'date':'1/1/2022', 'state': 'Pending'}, {'id':3, 'date':'1/2/2022', 'state': 'Pending'}]
    context = {'app_list': app_list}
    return render(request, 'seApp/appointmentManager.html', context)

def appointment(request, app_id):
    app = {'id':4, 'date':'1/1/2022', 'state': 'Pending'}
    context = {'app': app}
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
    return render(request,'seApp/browse.html')