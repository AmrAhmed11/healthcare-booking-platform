from django.shortcuts import render, redirect
from .models import Doctor, Appointment
from .forms import PrescriptionForm
from django.utils.dateparse import parse_datetime
from pytz import timezone
import pytz

# Create your views here.
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
    return render(request,'seApp/browse.html')