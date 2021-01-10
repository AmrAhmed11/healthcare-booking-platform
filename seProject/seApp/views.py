from django.shortcuts import render, redirect
from .forms import *
from django.utils.dateparse import parse_datetime
from pytz import timezone
import pytz
from datetime import datetime
from django.http import HttpResponse
from .models import *
from .forms import PrescriptionForm, CreatePatientForm, CreateDoctorForm, CreateStaffForm
from django.forms import inlineformset_factory
from django.contrib.auth.forms import  UserCreationForm
from django.contrib import messages
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.decorators import login_required
import string
from django.contrib.auth.models import Group



def loginpage (request):
    if request.user.is_authenticated:
        return redirect('seApp:home')
    else:
        if request.method=='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request,user)
                return redirect('seApp:home')
            else:
                messages.info(request,'Username or password is not correct')
                return render(request, 'seApp/login.html')
    return render(request, 'seApp/login.html')


def logoutuser (request):
    logout(request)
    return redirect ('seApp:loginpage')

#patient_registration
def register (request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form =  CreatePatientForm()
        
        if request.method == 'POST':
            form = CreatePatientForm(request.POST)
            if form.is_valid():
                user=form.save()
                group=Group.objects.get(name='patient')
                user.groups.add(group)
                messages.success(request,'Account is created successfully')
                return redirect('loginpage')
    context ={ 'form' : form }
    return render(request, 'seApp/register.html',context)

#Doctor_registration
def registerdoctor (request):
    if request.user.is_authenticated:
        return redirect('seApp:home')
    else:
        form =CreateDoctorForm()
        if request.method == 'POST':
            form =CreateDoctorForm(request.POST)
            if form.is_valid():
                user=form.save()
                group=Group.objects.get(name='doctor')
                user.groups.add(group)
                messages.success(request,'Account is created successfully')
                return redirect('seApp:loginpage')
    context ={ 'form' : form }
    return render(request, 'seApp/registerdoctor.html',context)
#Staff_registration
def registerstaff (request):
    if request.user.is_authenticated:
        return redirect('seApp:home')
    else:
        form =CreateStaffForm()
        if request.method == 'POST':
            form =CreateStaffForm(request.POST)
            if form.is_valid():
                user=form.save()
                messages.success(request,'Account is created successfully')
                return redirect('seApp:loginpage')
    context ={ 'form' : form }
    return render(request, 'seApp/registerstaff.html',context)



def index(request):
    return render(request, 'seApp/index.html')

def test(request):
    return render(request, 'seApp/test.html')

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

def doctorGetPatients(request):    
    doctor = Doctor.objects.get(id=1)
    app_list = doctor.appointment_set.all()
    patient_list = []
    for app in app_list:
        if app.patient not in patient_list:
            patient_list.append(app.patient)
    context = {'patients': patient_list}        
    return render(request, 'seApp/patients.html', context)


def doctorTransferPatient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)  
    doctors = Doctor.objects.all()
    if request.method == 'POST':
        timeslots = Doctor.objects.get(id=request.POST['newDoctor']).time_slots
        appointment = Appointment(
                patient = patient,
                doctor = Doctor.objects.get(id=request.POST['newDoctor']),
                status = 'Pending',
                time_slot =  timeslots[0],
                review = 'None',
                prescription = []
        )
        appointment.save()
        return redirect('seApp:patients')
    context = {'patient': patient, 'doctors': doctors}
    return render(request, 'seApp/patientsTransfer.html', context)
# ///////////////////////////////////////////////////////////////////////////////////////////
# FUNCTIONS WRITTEN BY LOAY 

#  MANAGING DOCTOR SERVICES 
def servicesManager(request):
    doctor = Doctor.objects.get(id=1)
    services_list = {'fees':doctor.fees, 'timeslots':doctor.time_slots,'description':doctor.description, 'medical_id':doctor.medical_id, 'specialization':doctor.specialization }
    context = {'services_list': services_list}
    return render(request, 'seApp/servicesManager.html', context)

#  CHANGING DOCTOR FEES ACTION
def changeFeeDoctor(request):
    fee = request.POST['fees']
    doctor = Doctor.objects.get(id=1)
    doctor.fees = fee
    doctor.save()
    return redirect('seApp:servicesManager')


# CHANGING DOCTOR MEDICAL DETAILS
def changeMedicalDetailsDoctor(request):
    description = request.POST['description']
    specialization = request.POST['specialization']
    medicalId = request.POST['medicalId']
    doctor = Doctor.objects.get(id=1)
    doctor.description = description
    doctor.specialization = specialization
    doctor.medical_id = medicalId
    doctor.save()
    return redirect('seApp:servicesManager')

# DELETE TIMESLOTS FOR DOCTOR ACTION
def deleteTimeslotDoctor(request):
    timeslot = request.POST['timeslot']
    print(timeslot)
    doctor = Doctor.objects.get(id=1)
    timeslotParsed = parse_datetime(timeslot) 
    doctor.time_slots.remove(timeslotParsed)
    doctor.save()
    return redirect('seApp:servicesManager')


# ADD TIMESLOTS FOR DOCTOR ACTION
def addTimeslotDoctor(request):
    timeslot = request.POST['timeslot']
    #checking if time is in the past
    if((parse_datetime(timeslot) - datetime.now()).total_seconds() < 0):
        return redirect('seApp:servicesManager')
    doctor = Doctor.objects.get(id=1)
    doctor.time_slots.append(timeslot)
    doctor.save()
    return redirect('seApp:servicesManager')


# RENDERDING DOCTOR STAFF MANAGER
def staffManager(request):
    staff_list = Staff.objects.filter(doctor=1)
    user_list = UserProfile.objects.all()
    staffToBeAdded_list = []
    for user in user_list:
        if not Patient.objects.filter(user=user.id) and not Doctor.objects.filter(user=user.id) and not Staff.objects.filter(user=user.id):
            staffToBeAdded_list.append(user)
    context = {'staff_list': staff_list,'staffToBeAdded_list': staffToBeAdded_list}
    return render(request, 'seApp/staffManager.html', context)


# ADDING NEW STAFF FOR DOCTOR ACTION 
def addNewStaff(request):
    staff = request.POST['staff']
    # staffObject = Staff.objects.get(user=staff)
    staffObject = Staff()
    staffObject.user = UserProfile.objects.get(id=staff)
    staffObject.specialization = "nurse"
    staffObject.doctor = Doctor.objects.get(id=1)
    staffObject.save()
    return redirect('seApp:staffManager')


#REMOVING NEW STAFF FOR DOCTOR ACTION
def removeStaff(request):
    staff = request.POST['staff']
    staffObject = Staff.objects.get(user=staff)
    staffObject.delete()
    return redirect('seApp:staffManager')


# ///////////////////////////////////////////////////////////////////////////////////////////



def browse(request):
    doctors = Doctor.objects.all()
    context = {'doctors':doctors}
    return render(request,'seApp/browse.html', context)

def appointmentUser(request, user_id):
    patient = Patient.objects.get(id=user_id)
    app_all= patient.appointment_set.all()
    app_pending =patient.appointment_set.filter(status="Pending")
    app_done = patient.appointment_set.filter(status="Done")
    app_cancelled = patient.appointment_set.filter(status="Cancelled")

    context = {'app_pending': app_pending,'app_done': app_done,'app_cancelled': app_cancelled, 'app_all' : app_all}

    return render(request, 'seApp/appointmentUser.html', context)    

def appointmentView(request, app_id):
    appointment = Appointment.objects.get(id=app_id)
   

    context = {'appointment': appointment}
    if appointment.status == 'Pending':
        
       if request.method == 'POST':
           appointment.status = "Cancelled"
           appointment.save()
           return render(request, 'seApp/appointmentcancelled.html', context)  


       return render(request, 'seApp/appointmentpending.html', context) 

    if appointment.status == 'Done':
       return render(request, 'seApp/appointmentdone.html', context)  

    else:
       return render(request, 'seApp/appointmentcancelled.html', context)  

    
def viewprescription(request, app_id ) :
    appointment = Appointment.objects.get(id=app_id)

    context = {'appointment': appointment}

    return render(request, 'seApp/viewprescription.html', context)      

def review(request, app_id ) :
    form = ReviewForm()
    formrate = RateForm()
    app = Appointment.objects.get(id=app_id)
    form = ReviewForm(instance=app)
    formrate = RateForm(instance=app.doctor)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=app)  
        formrate = RateForm(request.POST, instance=app.doctor)     
        if form.is_valid():
            form.save()
            #return redirect('appointmentView')

        if formrate.is_valid():
            formrate.save()
            #return redirect('appointmentView')
       

   
    context = {'app': app, 'form': form, 'formrate': formrate}
    return render(request, 'seApp/review.html', context)     



def viewDoctor(request, doctor_id):
    doctors = Doctor.objects.get(id = doctor_id)
    patient = Patient.objects.get(id = 1)
    if request.method == 'POST':
        appointment = Appointment(
                patient = patient,
                doctor = doctors,
                status = 'Pending',
                time_slot = request.POST.get('time'),
                review = 'None',
                prescription = []
        )
        appointment.save()
    context = {'doctors':doctors,}
    return render(request, 'seApp/viewDoctor.html', context)
    

