from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .forms import *
from django.utils.dateparse import parse_datetime
from pytz import timezone
import pytz
from datetime import datetime
from django.http import HttpResponse
from .models import *
from .forms import CreateUserForm, editProfileForm, updateProfileForm
from django.forms import inlineformset_factory
from django.contrib.auth.forms import *
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import string
from django.contrib.auth.models import Group
from django.utils import timezone
from .decorators import *
from . filters import DoctorFilter
from .mail import *

@unauthenticted_user
def loginpage (request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request,user)
            if user.role == "patient":
                return redirect('seApp:browse')
            elif user.role == "doctor":
                return redirect('seApp:servicesManager')
            elif user.role == "staff":
                return redirect('seApp:staffGetDetails')
            else:
                return redirect('seApp:collectedInfoAdmin')
        else:
            messages.info(request,'Username or password is not correct')
            return render(request, 'seApp/login.html')
    return render(request, 'seApp/login.html')

@login_required(login_url='seApp:loginpage')
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
                return redirect("seApp:UserProfile")
            elif(user.role == 'doctor'):
                group=Group.objects.get(name='doctor')
                user.groups.add(group)
                new_doctor = authenticate(username=form.cleaned_data['username'], 
                                            password=form.cleaned_data['password1'],
                                            )
                login(request, new_doctor)
                return redirect("seApp:servicesManager")
            elif(user.role == 'staff'):
                group=Group.objects.get(name='staff')
                user.groups.add(group)
                new_staff_member = authenticate(username=form.cleaned_data['username'], 
                                                password=form.cleaned_data['password1'],
                                                )
                login(request, new_staff_member)
                return redirect("seApp:staffGetDetails")

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
def appointmentGetManager(request):
    doctor = Doctor.objects.get(id=request.user.doctor.id)
    app_list = doctor.appointment_set.all()
    context = {'app_list': app_list}
    return render(request, 'seApp/appointmentManager.html', context)

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def postAppointment(request, app_id):
    app = Appointment.objects.get(id=app_id)
    index = int(request.POST['newTimeSlot'])
    app.time_slot = app.doctor.time_slots[index]
    app.doctor.time_slots.pop(index)
    app.save()
    app.doctor.save()
    patient = app.patient
    sendEmail('test',patient,'doctorEdit')
    return redirect('seApp:appointment', app_id=app_id)

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def deleteAppointment(request, app_id):
    app = Appointment.objects.get(id=app_id)
    app.status = 'Cancelled'
    app.save()
    patient = app.patient
    sendEmail('test',patient,'doctorCancel')
    return redirect('seApp:appointmentGetManager')

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
    specs = []
    for doctor in doctors:
        if doctor.specialization not in specs and doctor.specialization != None:
            specs.append(doctor.specialization)
    if request.method == 'POST':
        doctor = Doctor.objects.get(id=request.POST['doctor'])
        timeslot = request.POST['timeslot']
        appointment = Appointment(
                patient = patient,
                doctor = doctor,
                status = 'Pending',
                time_slot =  timeslot,
                review = 'None',
                prescription = []
        )
        timeslotParsed = parse_datetime(timeslot) 
        doctor.time_slots.remove(timeslotParsed)
        doctor.save()
        appointment.doctor.time_slots.pop(0)
        appointment.doctor.save()
        appointment.save()
        sendEmail('test',patient.user.email,'transferPatient')
        return redirect('seApp:patients')
    context = {'patient': patient, 'doctors': doctors,'specs':specs}
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
    return render(request, 'seApp/staffSpecialization.html')

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['staff'])
def staffPostDetails(request):
    staff = Staff.objects.get(id=request.user.staff.id)
    print(request.user.staff.id)
    staff.specialization = request.POST['specialization']
    staff.save()
    if staff.doctor is None:
        return redirect('seApp:staffGetDetails',)   
    else:
        return redirect('seApp:servicesManager')     

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['staff'])
def StaffProfile(request):
    staff = Staff.objects.get(id=request.user.staff.id)
    context = {'staff': staff}
    return render(request, 'seApp/staffProfile.html', context)



# ///////////////////////////////////////////////////////////////////////////////////////////
# FUNCTIONS WRITTEN BY LOAY 


# COLLECT ADMIN INFO
def collectedInfoAdmin(request):
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    clinics = Clinic.objects.all()
    staff = Staff.objects.all()
    payments = Payment.objects.all()
    apps = Appointment.objects.all()
    totalPaymentAmount = 0
    noPayments = payments.count()
    noDoctors = doctors.count()
    noPatients = patients.count()
    noStaff = staff.count()
    noClinics = clinics.count()
    noAppPending = 0
    noAppCancelled = 0
    noAppDone = 0
    noAppPaid = 0
    noApps = apps.count()
    for app in apps:
        if app.status == "Pending":
            noAppPending += 1
        elif app.status == "Cancelled":
            noAppCancel += 1
        elif app.status == "Done":
            noAppDone += 1
        else:
            noAppPaid += 1
    for payment in payments:
        totalPaymentAmount += payment.amount
    context = {'noPatients': noPatients, 'noAppPending': noAppPending, 'noAppCancelled': noAppCancelled, 'noAppDone': noAppDone,'noAppPaid': noAppPaid,'noApps':noApps,'noClinics':noClinics,'noStaff':noStaff,'noDoctors':noDoctors,'noPayments':noPayments,'totalPaymentAmount':totalPaymentAmount,
    'doctors':doctors,'patients':patients,'clinics':clinics,'staff':staff,'payments':payments,'apps':apps}
    return render(request, 'seApp/collectedInfoAdmin.html', context)
    



# COLLECT DOCTOR INFO
@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['staff', 'doctor'])
def collectedInfoDoctor(request):
    doctor = Doctor.objects.get(id=request.user.doctor.id)
    apps = doctor.appointment_set.all()
    patient_list = []
    reviews = []
    noPatients = 0
    noAppPending = 0
    noAppCancel = 0
    noAppDone = 0
    noAppPaid = 0
    for app in apps:
        if app.status == "Pending":
            noAppPending += 1
        elif app.status == "Cancelled":
            noAppCancel += 1
        elif app.status == "Done":
            noAppDone += 1
            reviews.append(app.review)
        else:
            noAppPaid += 1
        if app.patient not in patient_list:
            patient_list.append(app.patient)
            noPatients += 1
            
    totalApps = noAppCancel+noAppDone+noAppPaid+noAppPending
    context = {'noPatients': noPatients, 'noAppPending': noAppPending, 'noAppCancelled': noAppCancel, 'noAppDone': noAppDone,'noAppPaid': noAppPaid,'rating':request.user.doctor.rating,'reviews':reviews,'totalApps':totalApps}
    return render(request, 'seApp/collectedInfoDoctor.html', context)

    


#  MANAGING DOCTOR SERVICES 
@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['staff', 'doctor'])
def servicesManager(request):
    if request.user.role == 'staff':
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
    clinic = Clinic()
    clinic.save()
    doctorObject.clinic = clinic
    doctorObject.save()
    return redirect('seApp:staffManager')

# ///////////////////////////////////////////////////////////////////////////////////////////


@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['patient'])
def browse(request):
    doctors = Doctor.objects.all()
    myFilter = DoctorFilter(request.GET,queryset=doctors)
    doctors = myFilter.qs
    context = {'doctors':doctors , 'myFilter':myFilter}
    return render(request,'seApp/browse.html', context)

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['patient'])
def appointmentUser(request):

    patient = Patient.objects.get(id=request.user.patient.id)
    app_all= patient.appointment_set.all()
    app_pending =patient.appointment_set.filter(status="Pending")
    app_paid=patient.appointment_set.filter(status="Paid")
    app_done = patient.appointment_set.filter(status="Done")
    app_cancelled = patient.appointment_set.filter(status="Cancelled")

    context = {'app_pending': app_pending,'app_done': app_done,'app_cancelled': app_cancelled,'app_all':app_all,'app_paid':app_paid}

    return render(request, 'seApp/appointmentUser.html', context)   
 

 
    
@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['patient'])
def appointmentView(request, app_id):
                appointment = Appointment.objects.get(id=app_id)

                form = ReviewForm()
                app = Appointment.objects.get(id=app_id)
                form = ReviewForm(instance=app)

                context = {'appointment': appointment ,'app': app, 'form': form}
                if appointment.status == 'Paid':
                   if request.method == 'POST':
                        doctor = appointment.doctor.user.email
                        if 'cancel' in request.POST:
                          appointment.status = "Cancelled"
                          appointment.save()
                          timeslots = appointment.time_slot
                          appointment.doctor.time_slots.append(timeslots)
                          appointment.doctor.save()
                          sendEmail('test',doctor,'appointmentCancel')
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
                            timeslotnew =request.POST['appointment']
                            timeslotParsed = parse_datetime(timeslotnew) 
                            appointment.doctor.time_slots.remove(timeslotParsed)
                            appointment.doctor.save()
                            appointmentnew = Appointment(
                                patient = appointment.patient,
                                doctor = appointment.doctor,
                                status = 'Pending',
                                time_slot = timeslotnew,
                                review = 'None',
                                prescription = []
                            )
                            appointmentnew.save()
                            sendEmail('test',doctor,'appointmentEdit')
                            return render(request, 'seApp/appointmentcancelled.html', context)  
             
        

                   return render(request, 'seApp/appointmentpaid.html', context)

                if(appointment.status == 'Done'):

                    if request.method == 'POST':
                        if 'submit' in request.POST:
                            form = ReviewForm(request.POST,instance=app)
                            tempRating = int(request.POST['rate'])
                            if tempRating == 5:
                                rating = app.doctor.rating + 0.2
                            elif tempRating == 4:
                                rating = app.doctor.rating + 0.1
                            elif tempRating == 2:
                                rating = app.doctor.rating - 0.1
                            elif tempRating == 1:
                                rating = app.doctor.rating - 0.2
                            else:
                                rating = app.doctor.rating
                            app.doctor.rating = 5 if rating > 5  else rating
                            app.doctor.save()

                            if form.is_valid():
                                form.save()
                    return render(request, 'seApp/appointmentdone.html',context)

                else:
                  return render(request, 'seApp/appointmentcancelled.html', context)
                  
  
    
@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['patient'])    
def viewprescription(request, app_id ) :
        
    appointment = Appointment.objects.get(id=app_id)
    context = {'appointment': appointment}

    return render(request, 'seApp/viewprescription.html', context)      

   


@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['patient'])   
def viewDoctor(request, doctor_id):
    doctors = Doctor.objects.get(id=doctor_id)
    doctorEmail = doctors.user.email
    doctorAppointments = []
    doctorAppointments =Appointment.objects.filter(doctor__id = doctor_id )
    reviews = []
    for app in doctorAppointments:
        reviews.append(app.review)
    timeslots = []
    for timeslot in doctors.time_slots:
        if((timeslot - timezone.now()).total_seconds() > 0):
            timeslots.append(timeslot)
    doctors.time_slots = timeslots
    doctors.save()
    # if request.method == 'POST':
    #     if request.user.is_authenticated:
    #         role = request.user.role
    #         if(role == "patient"):
    #             patient = Patient.objects.get(id=request.user.patient.id)
    #             timeslots = doctors.time_slots
    #             timeslot = timeslots[int(request.POST['appointment']) - 1]
    #             doctors.time_slots.remove(timeslot)
    #             doctors.save()
    #             sendEmail('test',doctorEmail,'appointmentBook')
    #         else:
    #             return render(request, 'seApp/test.html')
    #     else:
    #         return render(request, 'seApp/login.html')
    context = {'doctors':doctors,'reviews':reviews}
    return render(request, 'seApp/viewDoctor.html', context)

@login_required(login_url='seApp:loginpage')
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

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['patient']) 
def paymentComplete(request, doctor_id):
    body = json.loads(request.body)
    print('BODY:', body)
    
    patient = Patient.objects.get(id=request.user.patient.id)
    doctor = Doctor.objects.get(id=doctor_id)
    doctorEmail = doctor.user.email

    if body['status'] == 'completed':
        if body['user'] == '1':
            appointment = Appointment(
                patient = patient,
                doctor = doctor,
                status = 'Paid',
                time_slot = body['timeSlot'],
                review = 'None',
                prescription = [],
                patient_name = patient.user,
            )
            timeslotParsed = parse_datetime(body['timeSlot']) 
            doctor.time_slots.remove(timeslotParsed)
            doctor.save()
            sendEmail('test',doctorEmail,'appointmentBook')
            appointment.save()
            return JsonResponse('Payment Completed!', safe=False)
        else:
            appointment = Appointment(
                patient = patient,
                doctor = doctor,
                status = 'Paid',
                time_slot = body['timeSlot'],
                review = 'None',
                prescription = [],
                patient_name = body['firstName'] + ' ' + body['lastName'],
            ) 
            timeslotParsed = parse_datetime(body['timeSlot']) 
            doctor.time_slots.remove(timeslotParsed)
            doctor.save()
            sendEmail('test',doctorEmail,'appointmentBook')
            appointment.save()
            return JsonResponse('Payment Completed!', safe=False)


# def editProfile(request):
#     if request.method == 'POST':
#         form = editProfileForm(request.POST, instance=request.user)
#         if form.is_valid:
#             form.save()
#             return redirect('/user/profile')

#     else:
#         form = editProfileForm(instance=request.user)
#         args = {'form':form}
#         return render(request, 'seApp/editProfile.html', args)
@login_required(login_url='seApp:loginpage')
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        update_session_auth_hash(request, form.user)
        if form.is_valid:
            form.save()
            return redirect('/user/profile')
        else:
            return redirect('/user/change-password')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request, 'seApp/changepassword.html', args)

@login_required(login_url='seApp:loginpage')
def updateProfile(request):
    if request.method == 'POST':
        form = updateProfileForm(request.POST, instance=request.user)
        if request.user.role == "patient":
            medical_history =  medicalHistoryForm(request.POST, instance=request.user.patient)
            context = {'form':form, 'medical_history':medical_history}
            if form.is_valid and medical_history.is_valid:
                form.save()
                medical_history.save()
                return redirect('/user/profile')

        if request.user.role == "doctor":
            context = {'form':form}
            if form.is_valid:
                form.save()
                return redirect('/doctor/profile')
    else:
        form = updateProfileForm(instance=request.user)
        if request.user.role == "patient":
            medical_history =  medicalHistoryForm(instance=request.user.patient)
            context = {'form':form, 'medical_history':medical_history}
        if request.user.role == "doctor":
            context = {'form':form}
        return render(request, 'seApp/updateProfile.html', context)