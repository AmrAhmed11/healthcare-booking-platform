from django.shortcuts import render, redirect, get_object_or_404
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
from django.contrib.auth.forms import  UserCreationForm, PasswordChangeForm
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
from django.contrib import messages

@unauthenticted_user
def loginpage (request):
""" Login Handler.

Performers authentication on login attempt and redirects every user
to the next page based on the role

:param incoming request
:return: login.html render
         redirect to browse route
         redirect to seApp:servicesManager route
         redirect to seApp:collectedInfoAdmin route
"""
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
""" Logout Handler.

Destroys user session on logout request

:param incoming request
:return: seApp:home
"""
    logout(request)
    return redirect ('seApp:home')

#patient_registration
@unauthenticted_user
def register (request):
""" Registraion Handler.

Creates a new user based in the input date in the registraion

:param incoming request
:return: seApp:UserProfile route
         seApp:servicesManager route
         seApp:staffGetDetails route
"""    
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
""" Home Page Render.

Renders home page upon request

:param incoming request
:return: seApp/index.html

"""       
    return render(request, 'seApp/index.html')


@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def appointmentGetManager(request):
""" GET all appointments.

Gets all authenticated doctor appointments

:param incoming request
:return: seApp/appointmentManager.html

"""       
    doctor = Doctor.objects.get(id=request.user.doctor.id)
    app_list = doctor.appointment_set.all()
    context = {'app_list': app_list}
    return render(request, 'seApp/appointmentManager.html', context)

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def postAppointment(request, app_id):
""" Appointment Date.

Changes appoinment date from a selected appointment date sent by
a POST request

:param incoming request
:return: eApp:appointment route

"""       
    app = get_object_or_404(Appointment, pk=app_id)
    index = int(request.POST['newTimeSlot'])
    app.time_slot = app.doctor.time_slots[index]
    app.doctor.time_slots.pop(index)
    app.save()
    app.doctor.save()
    patient = app.patient
    sendEmail('test',patient,'doctorEdit')
    messages.success(request, 'Appointment Date Changed Successfully.')
    return redirect('seApp:appointment', app_id=app_id)

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def doneAppointment(request, app_id):
""" Appointment State done.

Changes appoinment state to Done from POST request

:param incoming request
:return: appointmentGetManager route

"""           
    app = get_object_or_404(Appointment, pk=app_id)
    app.status = 'Done'
    app.save()
    patient = app.patient
    sendEmail('Appointment Done',patient,'doctorCancel')
    messages.success(request, 'Appointment Status Changed Successfully.')
    return redirect('seApp:appointmentGetManager')

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def deleteAppointment(request, app_id):
""" Appointment State cancelled.

Changes appoinment state to Cancelled from POST request

:param incoming request
       appointment id
:return: appointmentGetManager route

"""     
    app = get_object_or_404(Appointment, pk=app_id)
    app.status = 'Cancelled'
    app.save()
    patient = app.patient
    sendEmail('Appointment Cancelled',patient,'doctorCancel')
    messages.success(request, 'Appointment Cancelled Successfully.')
    return redirect('seApp:appointmentGetManager')

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def appointment(request, app_id):
""" Appointment Details.

Returns all appointments details from a selected 

:param incoming request
       appointment id
:return: appointment.html

""" 
    app = get_object_or_404(Appointment, pk=app_id)
    patient_account_name = app.patient.user.first_name + ' ' + app.patient.user.last_name
    context = {'app': app, 'doctor': app.doctor, 'patient': app.patient, 'patient_account_name':patient_account_name}
    return render(request, 'seApp/appointment.html', context)

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def doctorPostPrescription(request, app_id):
""" Add Prescription.

Adds a new medication to the appointment prescription list upon a POST requset

:param incoming request
       appointment id
:return: seApp:appointment route

"""     
    app = get_object_or_404(Appointment, pk=app_id)
    newMedication = request.POST['newMedication']
    if(app.prescription == None):
        app.prescription = []
    app.prescription.append(newMedication)
    app.save()
    messages.success(request, 'Prescription Added Successfully.')
    return redirect('seApp:appointment', app_id=app_id)

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def doctorDeletePrescription(request, app_id):
""" Delete Prescription.

Deletes a selected medication to the appointment prescription list upon a POST requset

:param incoming request
       appointment id
:return: seApp:appointment route

"""         
    app = get_object_or_404(Appointment, pk=app_id)
    deletedMedication = request.POST['deletedMedication']
    app.prescription.remove(deletedMedication)
    app.save()
    messages.success(request, 'Prescription Deleted Successfully.')
    return redirect('seApp:appointment', app_id=app_id)

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def doctorGetPatients(request):
""" All Patients.

Returns Authenticated user patients from the appointments list

:param incoming request
:return: patients.html

"""                
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
""" Transfer Patient.

Creates a new appontment between a selected patient and doctor Upon a POST requset
and returns a selected patient data Upon a GET request

:param incoming request
       patient_id
:return: patientsTransfer.html

"""             
    patient = get_object_or_404(Patient, pk=patient_id)  
    doctors = Doctor.objects.all()
    specs = []
    doctorsWithTimeSlots = []
    for doctor in doctors:
        if doctor.specialization not in specs and doctor.specialization != None:
            specs.append(doctor.specialization)
        if doctor.time_slots and doctor.id != request.user.doctor.id:
            doctorsWithTimeSlots.append(doctor)
    if request.method == 'POST':
        doctor = Doctor.objects.get(id=request.POST['doctor'])
        timeslot = request.POST['timeslot']
        index = int(timeslot) -1
        appointment = Appointment(
                patient = patient,
                doctor = doctor,
                status = 'Pending',
                time_slot =  doctor.time_slots[index],
                review = 'None',
                prescription = [],
                patient_name = patient,
        ) 
        doctor.time_slots.pop(index)
        doctor.save()
        appointment.save()
        sendEmail('test',patient.user.email,'transferPatient')
        messages.success(request, 'Patient Transferred Successfully.')
        return redirect('seApp:patients')
    context = {'patient': patient, 'doctors': doctorsWithTimeSlots,'specs':specs}
    return render(request, 'seApp/patientsTransfer.html', context)

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def DoctorProfile(request):
""" Doctor Profile.

Returns authenticated doctor personal data

:param incoming request
:return: doctorProfile.html

"""              
    doctor = Doctor.objects.get(id=request.user.doctor.id)
    context = {'doctor': doctor}
    return render(request, 'seApp/doctorProfile.html', context)

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['staff'])
def staffGetDetails(request):   
""" Staff Select Speclization.

Renders staff speclization selection page

:param incoming request
:return: staffSpecialization.html

"""         
    return render(request, 'seApp/staffSpecialization.html')

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['staff'])
def staffPostDetails(request):
""" Staff POST Select Speclization.

Sets the authenticated member speclization upon a POST request

:param incoming request
:return: seApp:servicesManager

"""       
    staff = Staff.objects.get(id=request.user.staff.id)
    staff.specialization = request.POST['specialization']
    staff.save()
    if staff.doctor is None:
        messages.warning(request, 'Please tell your doctor to add you.')    
        return redirect('seApp:staffGetDetails',)   
    else:
        return redirect('seApp:servicesManager')     

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['staff'])
def StaffProfile(request):
""" Staff Profile.

Returns authenticated authenticated personal data

:param incoming request
:return: staffProfile.html

"""           
    staff = Staff.objects.get(id=request.user.staff.id)
    context = {'staff': staff}
    return render(request, 'seApp/staffProfile.html', context)


@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=[])
def collectedInfoAdmin(request):
""" Admin Information Collection.

Collects statistical data about the system and renders admin information page

:param incoming request
:return: seApp:CollectedInfoAdmin
"""
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
            noAppPending =noAppPending + 1
        elif app.status == "Cancelled":
            noAppCancel =noAppCancel + 1
        elif app.status == "Done":
            noAppDone =noAppDone + 1
        else:
            noAppPaid += 1
    for payment in payments:
        totalPaymentAmount = totalPaymentAmount + payment.amount
    context = {'noPatients': noPatients, 'noAppPending': noAppPending, 'noAppCancelled': noAppCancelled, 'noAppDone': noAppDone,'noAppPaid': noAppPaid,'noApps':noApps,'noClinics':noClinics,'noStaff':noStaff,'noDoctors':noDoctors,'noPayments':noPayments,'totalPaymentAmount':totalPaymentAmount,
    'doctors':doctors,'patients':patients,'clinics':clinics,'staff':staff,'payments':payments,'apps':apps}
    return render(request, 'seApp/collectedInfoAdmin.html', context)
    

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['staff', 'doctor'])
def collectedInfoDoctor(request):
""" Doctor Information Collection.

Collects statistical data about the system and renders admin information page

:param incoming request
:return: seApp:collectedInfoDoctor
"""
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


@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['staff', 'doctor'])
def servicesManager(request):
""" Doctor Services Manager.

Returns doctor services details

:param incoming request
:return: seApp:servicesManager
"""
    if request.user.role == 'staff':
        doctor = Doctor.objects.get(id=request.user.staff.doctor.id)
    else:
        doctor = Doctor.objects.get(id=request.user.doctor.id)
    services_list = {'fees':doctor.fees, 'timeslots':doctor.time_slots,'description':doctor.description, 'medical_id':doctor.medical_id, 'specialization':doctor.specialization, 'clinic':doctor.clinic }
    context = {'services_list': services_list}
    return render(request, 'seApp/servicesManager.html', context)


@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def createNewClinic(request):
""" Create New Clinic.

Creates a new clinic and returns a success message after creation 

:param incoming request
:return: seApp:servicesManager
"""
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
    messages.success(request, 'Clinic Created Successfully.')
    return redirect('seApp:servicesManager')


@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['staff', 'doctor'])
def changeFeeDoctor(request):
""" Doctor Change Fee Action.

Change doctor fee and return a success message upon saving

:param incoming request
:return: seApp:servicesManager
"""
    fee = request.POST['fees']
    doctor = Doctor.objects.get(id=request.user.doctor.id)
    doctor.fees = fee
    doctor.save()
    messages.success(request, 'Fees Changed Successfully.')
    return redirect('seApp:servicesManager')


@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['staff', 'doctor'])
def changeMedicalDetailsDoctor(request):
""" Change Doctor`s Medical Details.

Change doctor medical details and return a success message upon saving

:param incoming request
:return: seApp:servicesManager
"""
    description = request.POST['description']
    specialization = request.POST['specialization']
    medicalId = request.POST['medicalId']
    doctor = Doctor.objects.get(id=request.user.doctor.id)
    doctor.description = description
    doctor.specialization = specialization
    doctor.medical_id = medicalId
    doctor.save()
    messages.success(request, 'Medical Details Changed Successfully.')
    return redirect('seApp:servicesManager')


@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['staff', 'doctor'])
def deleteTimeslotDoctor(request):
""" Doctor Timeslot Deletion.

Deletes a timeslot chosen by doctor

:param incoming request
:return: seApp:servicesManager
"""
    timeslot = request.POST['timeslot']
    if(request.user.role=='staff'):
        doctor = Doctor.objects.get(id=request.user.staff.doctor.id)
    else:
        doctor = request.user.doctor
    timeslotParsed = parse_datetime(timeslot) 
    doctor.time_slots.remove(timeslotParsed)
    doctor.save()
    messages.success(request, 'Time Slot Deleted Successfully.')
    return redirect('seApp:servicesManager')


@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['staff', 'doctor'])
def addTimeslotDoctor(request):
""" Doctor Timeslot adding.

Adds a certain timeslot chosen by the doctor and returns a success message upon saving

:param incoming request
:return: seApp:servicesManager
"""
    timeslot = request.POST['timeslot']
    #checking if time is in the past
    if((parse_datetime(timeslot) - datetime.now()).total_seconds() < 0):
        messages.error(request, 'Can\'t add time slot in a past date.')
        return redirect('seApp:servicesManager')
    if(request.user.role=='staff'):
        doctor = Doctor.objects.get(id=request.user.staff.doctor.id)
    else:
        doctor = request.user.doctor
    if(doctor.time_slots == None):
        doctor.time_slots = []
    doctor.time_slots.append(timeslot)
    doctor.save()
    messages.success(request, 'Time slot added successfully.')
    return redirect('seApp:servicesManager')


@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def staffManager(request):
""" Doctor Staff Manager.

Collects staff info and returns staff manager 

:param incoming request
:return: seApp:staffManager
"""
    staff_list = Staff.objects.filter(doctor=request.user.doctor.id)
    user_list = Staff.objects.all()
    staffToBeAdded_list = []
    doctor_list = []
    doctor_new_list = []
    clinicOwner = 0
    clinicId = 0
    clinicTemp = 0
    if request.user.doctor.clinic:
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


@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def addNewStaff(request):
""" Doctor Add New Staff.

Adds a staff to a certain doctor and return a success message upon success

:param incoming request
:return: seApp:staffManager
"""
    staff = request.POST['staff']
    doctor = request.user.doctor
    staffObject = Staff.objects.get(id=staff)
    staffObject.doctor = doctor
    staffObject.save()
    messages.success(request, 'Staff Added Successfully.')
    return redirect('seApp:staffManager')


@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def removeStaff(request):
""" Doctor Remove Staff.

Deletes staff from a certain doctor and return a success message upon success

:param incoming request
:return: seApp:staffManager
"""
    staff = request.POST['staff']
    staffObject = Staff.objects.get(id=staff)
    staffObject.delete()
    messages.success(request, 'Staff Removed Successfully.')
    return redirect('seApp:staffManager')


@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def addNewDoctor(request):
""" Add New Doctor to a Clinic.

Add a certain doctor chosen by the clinic owner to this clinic and return a success message upon saving

:param incoming request
:return: seApp:staffManager
"""
    doctor = request.POST['doctor']
    clinic = request.POST['clinic']
    clinicObj = Clinic.objects.get(id=clinic)
    doctorObject = Doctor.objects.get(user_id=doctor)
    doctorObject.clinic = clinicObj
    doctorObject.save()
    messages.success(request, 'Doctor Added Successfully.')
    return redirect('seApp:staffManager')


@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['doctor'])
def removeDoctor(request):
""" Remove a Doctor from a Clinic.

Remove a certian doctor from a clinic and remove a success message upon saving 

:param incoming request
:return: seApp:staffManager
"""
    doctor = request.POST['doctor']
    doctorObject = Doctor.objects.get(user=doctor)
    clinic = Clinic()
    clinic.save()
    doctorObject.clinic = clinic
    doctorObject.save()
    messages.success(request, 'Doctor Removed Successfully.')
    return redirect('seApp:staffManager')




@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['patient'])
def browse(request):
""" Browse Doctors.

Returns all registered doctors and offers filtering 

:param incoming request
:return: browse.html

"""      
    doctors = Doctor.objects.all()
    doctorFiltered = []
    for doctor in doctors:
        if doctor.specialization != None and doctor.fees != None and doctor.medical_id != None:
            doctorFiltered.append(doctor)
    myFilter = DoctorFilter(request.GET,queryset=doctors)
    doctors = myFilter.qs
    context = {'doctors':doctorFiltered , 'myFilter':myFilter}
    return render(request,'seApp/browse.html', context)

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['patient'])
def appointmentUser(request):
""" Patient Appointments Manager .

Returns all patient`s appointments

:param incoming request
:return: seApp:appointmentUser
"""
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
""" Patient Appointment Actions.

Handles appointment status changing(Booking, Cancellation, Edit, Payment) and validation

:param incoming request
:return: seApp:appointmentDone
:return: seApp:appointmentCancel
:return: seApp:appointmentEdit
"""
    appointment = get_object_or_404(Appointment, pk=app_id)

    form = ReviewForm()
    app = get_object_or_404(Appointment, pk=app_id)
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

    if appointment.status == 'Pending':
        
        if request.method == 'POST':
            body = json.loads(request.body) 
            doctor = appointment.doctor.user.email
            if 'cancel' in request.POST:
                appointment.status = "Cancelled"
                appointment.save()
                timeslots = appointment.time_slot
                appointment.doctor.time_slots.append(timeslots)
                appointment.doctor.save()
                sendEmail('test',doctor,'appointmentCancel')
                return render(request, 'seApp/appointmentcancelled.html', context)  

            if body['status'] == 'completed':
                appointment.status = 'Paid'
                appointment.save()
                sendEmail('test',doctor,'appointmentEdit')
                return render(request, 'seApp/appointmentcancelled.html', context)  
    
        return render(request, 'seApp/appointmentcancelled.html', context)
    
    if(appointment.status == 'Done'):

        if request.method == 'POST':
            if 'submit' in request.POST:
                form = ReviewForm(request.POST,instance=app)
                tempRating = int(request.POST['rate'])
                if app.doctor.rating is None:
                    app.doctor.rating = 5
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
                #clinic rating
                totalRating = 0
                noDoctors = 0
                doctors = Doctor.objects.all()
                clinic = app.doctor.clinic
                for doctor in doctors:
                    if doctor.clinic == clinic:
                        totalRating = totalRating + doctor.rating
                        noDoctors += 1
                clinic.rating = (totalRating/noDoctors)
                clinic.save()

                    

                if form.is_valid():
                    form.save()
        return render(request, 'seApp/appointmentdone.html',context)

    else:
        return render(request, 'seApp/appointmentcancelled.html', context)
                  
  
    
@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['patient'])    
def viewprescription(request, app_id) :
""" View Prescription.

Returns all medication in a certain appointment prescription list

:param incoming request
       app_id
:return: viewprescription.html

"""          
    appointment = get_object_or_404(Appointment, pk=app_id)
    context = {'appointment': appointment}
    return render(request, 'seApp/viewprescription.html', context)      

   

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['patient'])   
def viewDoctor(request, doctor_id):
""" View Doctor.

Returns a selected doctor details upon GET request

:param incoming request
       doctor_id
:return: viewDoctor.html

"""         
    doctors = get_object_or_404(Doctor, pk=doctor_id)
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
    context = {'doctors':doctors,'reviews':reviews}
    return render(request, 'seApp/viewDoctor.html', context)

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['patient']) 
def UserProfile(request):
""" User Profile.

Returns authenticated patient personal data

:param incoming request
:return: userProfile.html

"""            
    patient = Patient.objects.get(id = request.user.patient.id)
    context = {'patient':patient}
    return render(request, 'seApp/userProfile.html', context)

@login_required(login_url='seApp:loginpage')
@allowed_users(allowed_roles=['patient']) 
def paymentComplete(request, doctor_id):
""" Payments.

Checks valid payments through Paypal gateway

:param incoming request
       doctor_id

"""      
    body = json.loads(request.body)
    
    patient = Patient.objects.get(id=request.user.patient.id)
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    doctorEmail = doctor.user.email

    if body['status'] == 'completed':
        if body['user'] == '1':
            timeslots = doctor.time_slots
            timeslot = timeslots[int(body['timeSlot']) - 1]
            appointment = Appointment(
                patient = patient,
                doctor = doctor,
                status = 'Paid',
                time_slot = timeslot,
                review = 'None',
                prescription = [],
                patient_name = patient.user.first_name + ' ' + patient.user.last_name,
            )
            doctor.time_slots.remove(timeslot)
            doctor.save()
            sendEmail('test',doctorEmail,'appointmentBook')
            appointment.save()
            messages.success(request, 'Payment Successful.')
            return redirect('/user/appointment')
        else:
            timeslots = doctor.time_slots
            timeslot = timeslots[int(body['timeSlot']) - 1]
            appointment = Appointment(
                patient = patient,
                doctor = doctor,
                status = 'Paid',
                time_slot = timeslot,
                review = 'None',
                prescription = [],
                patient_name = body['firstName'] + ' ' + body['lastName'],
            ) 
            doctor.time_slots.remove(timeslot)
            doctor.save()
            sendEmail('test',doctorEmail,'appointmentBook')
            appointment.save()
            messages.success(request, 'Payment Successful.')
            return redirect('/user/appointment')

@login_required(login_url='seApp:loginpage')
def changePassword(request):
""" Change Passowrd.

Takes a new password from the user and checks if the old password is valid 
it changes the user request

:param incoming request
:return: changePassword.html

"""     
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            if request.user.role == 'patient':
                messages.success(request, 'Profile Edited Successfully.')
                return redirect('/user/profile')
            else:
                messages.success(request, 'Profile Edited Successfully.')
                return redirect('/doctor/profile')
        else:
            messages.error(request, 'Incorrect password')
            return redirect('/accounts/change_password')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request, 'seApp/changePassword.html', args)

@login_required(login_url='seApp:loginpage')
def updateProfile(request):
""" Update Profile Info.

Takes a new info upon a POST request from the authenticated user (doctor or patient) and update the
personal info

:param incoming request
:return: updateProfile.html

"""        
    if request.method == 'POST':
        form = updateProfileForm(request.POST, instance=request.user)
        if request.user.role == "patient":
            medical_history =  medicalHistoryForm(request.POST, instance=request.user.patient)
            context = {'form':form, 'medical_history':medical_history}
            if form.is_valid and medical_history.is_valid:
                form.save()
                medical_history.save()
                messages.success(request, 'Profile Edited Successfully.')
                return redirect('/user/profile')

        if request.user.role == "doctor":
            context = {'form':form}
            if form.is_valid:
                form.save()
                messages.success(request, 'Profile Edited Successfully.')
                return redirect('/doctor/profile')
    else:
        form = updateProfileForm(instance=request.user)
        if request.user.role == "patient":
            medical_history =  medicalHistoryForm(instance=request.user.patient)
            context = {'form':form, 'medical_history':medical_history}
        if request.user.role == "doctor":
            context = {'form':form}
        return render(request, 'seApp/updateProfile.html', context)

def emergency(request,doctor_id):
""" Emergancy.

Creates an appointment between the authenticated user and a selected doctor 
and selects the closest time slot availble

:param incoming request
       doctor_id
:return: viewappointment.html

"""         
    if request.method == 'POST':
        doctor = get_object_or_404(Doctor, pk=doctor_id)
        timeslots = doctor.time_slots
        timeslots.sort()
        if timeslots:
            timeslot = timeslots[0]
            appointment = Appointment(
                patient = request.user.patient,
                doctor = doctor,
                status = 'Pending',
                time_slot = timeslot,
                review = 'None',
                prescription = [],
                patient_name = request.user,
            )
            doctor.time_slots.remove(timeslot)
            doctor.save()
            appointment.save()
            messages.success(request, 'Emergency Appointment Booked Successfully.')
            return redirect('/user/appointment')

