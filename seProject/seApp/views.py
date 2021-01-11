from django.shortcuts import render, redirect
from .forms import *
from django.utils.dateparse import parse_datetime
from pytz import timezone
import pytz
from datetime import datetime
from django.http import HttpResponse
from .models import *
from .forms import CreateUserForm
from django.forms import inlineformset_factory
from django.contrib.auth.forms import  UserCreationForm
from django.contrib import messages
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.decorators import login_required
import string
from django.contrib.auth.models import Group
from django.utils import timezone
from .decorators import *

@unauthenticted_user
def loginpage (request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('seApp:test')
        else:
            messages.info(request,'Username or password is not correct')
            return render(request, 'seApp/login.html')
    return render(request, 'seApp/login.html')


def logout_path (request):
    logout(request)
    return redirect ('seApp:home')

#patient_registration
@unauthenticted_user
def register (request):
    form =  CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            if(user.role == 'patient'):
                group=Group.objects.get(name='patient')
                user.groups.add(group)
                new_patient = authenticate(username=form.cleaned_data['username'], 
                                            password=form.cleaned_data['password1'],
                                            )
                login(request, new_patient)
                return redirect("seApp:test")
            elif(user.role == 'doctor'):
                group=Group.objects.get(name='doctor')
                user.groups.add(group)
                new_doctor = authenticate(username=form.cleaned_data['username'], 
                                            password=form.cleaned_data['password1'],
                                            )
                login(request, new_doctor)
                return redirect("seApp:test")
            elif(user.role == 'staff'):
                group=Group.objects.get(name='staff')
                user.groups.add(group)
                new_staff_member = authenticate(username=form.cleaned_data['username'], 
                                                password=form.cleaned_data['password1'],
                                                )
                login(request, new_staff_member)
                return redirect("seApp:test")

    context ={ 'form' : form }
    return render(request, 'seApp/register.html',context)

@unauthenticted_user
def index(request):
    return render(request, 'seApp/index.html')

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def test(request):
    return render(request, 'seApp/test.html')

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def appointmentManager(request):
    doctor = Doctor.objects.get(id=request.user.doctor.id)
    app_list = doctor.appointment_set.all()
    context = {'app_list': app_list}
    return render(request, 'seApp/appointmentManager.html', context)

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def appointment(request, app_id):
    app = Appointment.objects.get(id=app_id)
    context = {'app': app, 'doctor': app.doctor, 'patient': app.patient}
    return render(request, 'seApp/appointment.html', context)

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def doctorPostPrescription(request, app_id):
    app = Appointment.objects.get(id=app_id)
    newMedication = request.POST['newMedication']
    if(app.prescription == None):
        app.prescription = []
    app.prescription.append(newMedication)
    app.save()
    return redirect('seApp:appointment', app_id=app_id)

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def doctorDeletePrescription(request, app_id):
    app = Appointment.objects.get(id=app_id)
    deletedMedication = request.POST['deletedMedication']
    app.prescription.remove(deletedMedication)
    app.save()
    return redirect('seApp:appointment', app_id=app_id)

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def doctorGetPatients(request):    
    doctor = Doctor.objects.get(id=request.user.doctor.id)
    app_list = doctor.appointment_set.all()
    patient_list = []
    for app in app_list:
        if app.patient not in patient_list:
            patient_list.append(app.patient)
    context = {'patients': patient_list}        
    return render(request, 'seApp/patients.html', context)

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
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

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def DoctorProfile(request):
    doctor = Doctor.objects.get(id=request.user.doctor.id)
    context = {'doctor': doctor}
    return render(request, 'seApp/doctorProfile.html', context)

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['staff'])
def staffGetDetails(request):   
    return render(request, 'seApp/staffSpecialization.html', context)

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['staff'])
def staffPostDetails(request):
    staff = Staff.objects.get(id=request.user.staff.id)
    staff.specialization = request.POST['staffSpecialization']
    staff.save()
    if staff.doctor is None:
        return redirect('seApp:staffGetDetails',)   
    else:
        return redirect('seApp:servicesManager', doctor_id = staff.doctor.id)     





# ///////////////////////////////////////////////////////////////////////////////////////////
# FUNCTIONS WRITTEN BY LOAY 


#  MANAGING DOCTOR SERVICES 
@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['staff', 'doctor'])
def servicesManager(request):
    if request.user.role is 'staff':
        doctor = Doctor.objects.get(id=request.user.staff.doctor.id)
    else:
        doctor = Doctor.objects.get(id=request.user.doctor.id)
    services_list = {'fees':doctor.fees, 'timeslots':doctor.time_slots,'description':doctor.description, 'medical_id':doctor.medical_id, 'specialization':doctor.specialization, 'clinic':doctor.clinic }
    context = {'services_list': services_list}
    return render(request, 'seApp/servicesManager.html', context)

# CREATE NEW CLINIC ACTION
@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def createNewClinic(request):
    clinicName = request.POST['clinicName']
    clinicAddress = request.POST['clinicAddress']
    clinic = Clinic()
    clinic.name = clinicName
    clinic.address = clinicAddress
    clinic.owner_id = request.user.id
    clinic.rating = 0
    doctor = Doctor.objects.get(id=request.user.doctor.id)
    doctor.clinic = clinic
    clinic.save()
    doctor.save()
    return redirect('seApp:servicesManager')


#  CHANGING DOCTOR FEES ACTION
@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['staff', 'doctor'])
def changeFeeDoctor(request):
    fee = request.POST['fees']
    doctor = Doctor.objects.get(id=request.user.doctor.id)
    doctor.fees = fee
    doctor.save()
    return redirect('seApp:servicesManager')


# CHANGING DOCTOR MEDICAL DETAILS
@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['staff', 'doctor'])
def changeMedicalDetailsDoctor(request):
    description = request.POST['description']
    specialization = request.POST['specialization']
    medicalId = request.POST['medicalId']
    doctor = Doctor.objects.get(id=request.user.doctor.id)
    doctor.description = description
    doctor.specialization = specialization
    doctor.medical_id = medicalId
    doctor.save()
    return redirect('seApp:servicesManager')

# DELETE TIMESLOTS FOR DOCTOR ACTION
@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['staff', 'doctor'])
def deleteTimeslotDoctor(request):
    timeslot = request.POST['timeslot']
    doctor = Doctor.objects.get(id=request.user.doctor.id)
    timeslotParsed = parse_datetime(timeslot) 
    doctor.time_slots.remove(timeslotParsed)
    doctor.save()
    return redirect('seApp:servicesManager')


# ADD TIMESLOTS FOR DOCTOR ACTION
@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['staff', 'doctor'])
def addTimeslotDoctor(request):
    timeslot = request.POST['timeslot']
    #checking if time is in the past
    if((parse_datetime(timeslot) - datetime.now()).total_seconds() < 0):
        return redirect('seApp:servicesManager')
    doctor = Doctor.objects.get(id=request.user.doctor.id)
    if(doctor.time_slots == None):
        doctor.time_slots = []
    doctor.time_slots.append(timeslot)
    doctor.save()
    return redirect('seApp:servicesManager')


# RENDERDING DOCTOR STAFF MANAGER
@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def staffManager(request):
    staff_list = Staff.objects.filter(doctor=request.user.doctor.id)
    user_list = Staff.objects.all()
    staffToBeAdded_list = []
    doctor_list = []
    doctor_new_list = []
    clinicOwner = 0
    clinicId = 0
    clinicTemp = request.user.doctor.clinic.id 
    clinicId = clinicTemp
    clinic = Clinic.objects.get(id=clinicTemp)
    
    if clinic.owner_id == request.user.id:
        clinicOwner = 1
        doctors = Doctor.objects.all()
        for doctor in doctors:
            if doctor.clinic == None:
                
                doctor_new_list.append(doctor)
            elif doctor.clinic.id == clinicId:
                doctor_list.append(doctor)
                
    
    
    for user in user_list:
        if user.doctor == None:
            staffToBeAdded_list.append(user)

    
    context = {'staff_list': staff_list,'staffToBeAdded_list': staffToBeAdded_list, 'doctor_list': doctor_list, 'doctor_new_list':doctor_new_list,'clinicOwner':clinicOwner,'clinicId':clinicId}
    return render(request, 'seApp/staffManager.html', context)


# ADDING NEW STAFF FOR DOCTOR ACTION 
@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def addNewStaff(request):
    staff = request.POST['staff']
    doctor = Doctor.objects.get(id=request.user.doctor.id)
    staffObject = Staff.objects.get(user_id=staff)
    staffObject.doctor = doctor
    staffObject.save()
    return redirect('seApp:staffManager')


#REMOVING NEW STAFF FOR DOCTOR ACTION
@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def removeStaff(request):
    staff = request.POST['staff']
    staffObject = Staff.objects.get(user=staff)
    staffObject.delete()
    return redirect('seApp:staffManager')




# ADDING NEW DOCTOR FOR DOCTOR ACTION 
@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def addNewDoctor(request):
    doctor = request.POST['doctor']
    clinic = request.POST['clinic']
    clinicObj = Clinic.objects.get(id=clinic)
    doctorObject = Doctor.objects.get(user_id=doctor)
    doctorObject.clinic = clinicObj
    doctorObject.save()
    return redirect('seApp:staffManager')


#REMOVING DOCTOR FROM CLINIC ACTION
@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def removeDoctor(request):
    doctor = request.POST['doctor']
    doctorObject = Doctor.objects.get(user=doctor)
    doctorObject.clinic = ''
    doctorObject.save()
    return redirect('seApp:staffManager')

# ///////////////////////////////////////////////////////////////////////////////////////////



def browse(request):
    doctors = Doctor.objects.all()
    context = {'doctors':doctors}
    return render(request,'seApp/browse.html', context)

def appointmentUser(request):
 if request.user.is_authenticated:
        role = request.user.role
        if(role == 'patient'):
             patient = Patient.objects.get(id=request.user.patient.id)
             app_all= patient.appointment_set.all()
             app_pending =patient.appointment_set.filter(status="Pending")
             app_done = patient.appointment_set.filter(status="Done")
             app_cancelled = patient.appointment_set.filter(status="Cancelled")

             context = {'app_pending': app_pending,'app_done': app_done,'app_cancelled': app_cancelled,'app_all':app_all}

             return render(request, 'seApp/appointmentUser.html', context)   

        else :  
             return redirect('/')   

 else:
     return redirect('seApp:loginpage')
    

def appointmentView(request, app_id):
    if request.user.is_authenticated:
        role = request.user.role
        if(role == 'patient'):
                appointment = Appointment.objects.get(id=app_id)

                form = ReviewForm()
                app = Appointment.objects.get(id=app_id)
                form = ReviewForm(instance=app)

                context = {'appointment': appointment ,'app': app, 'form': form}
                if appointment.status == 'Pending':
                   if request.method == 'POST':
                       if 'cancel' in request.POST:
                          appointment.status = "Cancelled"
                          appointment.save()
                          timeslots = appointment.time_slot
                          appointment.doctor.time_slots.append(timeslots)
                          appointment.doctor.save()
                          return render(request, 'seApp/appointmentcancelled.html', context)  

                       if 'edit' in request.POST:
                           timeslots = []
                           for timeslot in appointment.doctor.time_slots:
                               if((timeslot - timezone.now()).total_seconds() > 0):
                                    timeslots.append(timeslot)
                           appointment.doctor.time_slots = timeslots
                           appointment.doctor.save() 

                           appointment.status = "Cancelled"
                           appointment.save()
                           timeslotadd = appointment.time_slot
                           appointment.doctor.time_slots.append(timeslotadd)
                           timeslot =request.POST['appointment']
                           #appointment.doctor.time_slots.remove(timeslot)
                           appointment.doctor.save()
                           appointmentnew = Appointment(
                                patient = appointment.patient,
                                doctor = appointment.doctor,
                                status = 'Pending',
                                time_slot = timeslot,
                                review = 'None',
                                prescription = []
                            )
                           appointmentnew.save()
                           return render(request, 'seApp/appointmentcancelled.html', context)  
             
        

                   return render(request, 'seApp/appointmentpending.html', context)

                if(appointment.status == 'Done'):

                    if request.method == 'POST':
                        if 'submit' in request.POST:
                            form = ReviewForm(request.POST,instance=app)
                            app.doctor.rating = request.POST['rate']
                            app.doctor.save()

                            if form.is_valid():
                                form.save()
                    return render(request, 'seApp/appointmentdone.html',context)

                else:
                  return render(request, 'seApp/appointmentcancelled.html', context)  
  

        else :  
             return redirect('/')   

    else:
     return redirect('seApp:loginpage')
    
    
def viewprescription(request, app_id ) :
    if request.user.is_authenticated:
        role = request.user.role
        if(role == 'patient'):
                appointment = Appointment.objects.get(id=app_id)

                context = {'appointment': appointment}

        else :
                return redirect('/')

    else:
     return redirect('seApp:loginpage')

    return render(request, 'seApp/viewprescription.html', context)      

   


    
def viewDoctor(request, doctor_id):
    doctors = Doctor.objects.get(id=doctor_id)
    timeslots = []
    for timeslot in doctors.time_slots:
        if((timeslot - timezone.now()).total_seconds() > 0):
            timeslots.append(timeslot)
    doctors.time_slots = timeslots
    doctors.save()
    if request.method == 'POST':
        if request.user.is_authenticated:
            role = request.user.role
            if(role == "patient"):
                patient = Patient.objects.get(id=request.user.patient.id)
                timeslots = doctors.time_slots
                timeslot = timeslots[int(request.POST['appointment']) - 1]
                doctors.time_slots.remove(timeslot)
                appointment = Appointment(
                    patient = patient,
                    doctor = doctors,
                    status = 'Pending',
                    time_slot = timeslot,
                    review = 'None',
                    prescription = []
                )
                appointment.save()
                doctors.save()
            else:
                return render(request, 'seApp/test.html')
        else:
            return render(request, 'seApp/login.html')
    context = {'doctors':doctors,}
    return render(request, 'seApp/viewDoctor.html', context)

def UserProfile(request):
    if request.user.is_authenticated:
        role = request.user.role
        if(role == "patient"):
            patient = Patient.objects.get(id = request.user.patient.id)
            context = {'patient':patient}
            return render(request, 'seApp/userProfile.html', context)
        else:
            return render(request, 'seApp/test.html')
    else:
        return render(request, 'seApp/login.html')




