from django.test import SimpleTestCase, TestCase, Client
from django.urls import resolve, reverse
from .views import *
from .models import *
from django.contrib.auth.models import *
# Url tests 
class TestUrls(SimpleTestCase):

    def test_home_url(self):
        url=reverse('seApp:home')
        self.assertEquals(resolve(url).func, index)

    def test_testpage_url(self):
        url=reverse('seApp:test')
        self.assertEquals(resolve(url).func, test)

    def test_patients_url(self):
        url=reverse('seApp:patients')
        self.assertEquals(resolve(url).func, doctorGetPatients)
    
    def test_staffManager_url(self):
        url=reverse('seApp:staffManager')
        self.assertEquals(resolve(url).func, staffManager)
    
    def test_servicesManager_url(self):
        url=reverse('seApp:servicesManager')
        self.assertEquals(resolve(url).func, servicesManager)

    def test_createNewClinic_url(self):
        url=reverse('seApp:createNewClinic')
        self.assertEquals(resolve(url).func, createNewClinic)
    
    def test_deleteTimeslotDoctor_url(self):
        url=reverse('seApp:deleteTimeslotDoctor')
        self.assertEquals(resolve(url).func, deleteTimeslotDoctor)
    
    def test_addNewStaff_url(self):
        url=reverse('seApp:addNewStaff')
        self.assertEquals(resolve(url).func, addNewStaff)
    
    def test_home_url(self):
        url=reverse('seApp:home')
        self.assertEquals(resolve(url).func, index)
    
    def test_removeStaff_url(self):
        url=reverse('seApp:removeStaff')
        self.assertEquals(resolve(url).func, removeStaff)
    
    def test_addNewDoctor_url(self):
        url=reverse('seApp:addNewDoctor')
        self.assertEquals(resolve(url).func,addNewDoctor)
    
    def test_removeDoctor_url(self):
        url=reverse('seApp:removeDoctor')
        self.assertEquals(resolve(url).func, removeDoctor)
    
    def test_addTimeslotDoctor_url(self):
        url=reverse('seApp:addTimeslotDoctor')
        self.assertEquals(resolve(url).func, addTimeslotDoctor)
    
    def test_addTimeslotDoctor_url(self):
        url=reverse('seApp:addTimeslotDoctor')
        self.assertEquals(resolve(url).func, addTimeslotDoctor)
    
    def test_changeMedicalDetailsDoctor_url(self):
        url=reverse('seApp:changeMedicalDetailsDoctor')
        self.assertEquals(resolve(url).func, changeMedicalDetailsDoctor)

    def test_changeFeeDoctor_url(self):
        url=reverse('seApp:changeFeeDoctor')
        self.assertEquals(resolve(url).func, changeFeeDoctor)

    def test_changeFeeDoctor_url(self):
        url=reverse('seApp:changeFeeDoctor')
        self.assertEquals(resolve(url).func, changeFeeDoctor)

    def test_DoctorProfile_url(self):
        url=reverse('seApp:DoctorProfile')
        self.assertEquals(resolve(url).func, DoctorProfile)

    def test_staffGetDetails_url(self):
        url=reverse('seApp:staffGetDetails')
        self.assertEquals(resolve(url).func, staffGetDetails)

    def test_staffPostDetails_url(self):
        url=reverse('seApp:staffPostDetails')
        self.assertEquals(resolve(url).func, staffPostDetails)

    def test_browse_url(self):
        url=reverse('seApp:browse')
        self.assertEquals(resolve(url).func, browse)
        
    def test_logout_url(self):
        url=reverse('seApp:logout')
        self.assertEquals(resolve(url).func, logout_path)
        
    def test_loginpage_url(self):
        url=reverse('seApp:loginpage')
        self.assertEquals(resolve(url).func, loginpage)
        
    def test_register_url(self):
        url=reverse('seApp:register')
        self.assertEquals(resolve(url).func, register)

class test_urls_pk (TestCase):
        
    def test_doctorTransferPatient_url(self):
        self.user=UserProfile.objects.create(
            first_name='loay',
            last_name='elshall',
            email='elshall@gmail.com',
            gender='Male',
            username='Elshall',
            role='patient'
        )
        self.patient=Patient.objects.create(user=self.user)
        patient_id=self.patient.id
        url=reverse('seApp:TransferPatients', args=[str(patient_id)])
        self.assertEquals (resolve(url).func, doctorTransferPatient)

    def test_PostPrescription_url(self):
        self.user=UserProfile.objects.create(
            first_name='loay',
            last_name='elshall',
            email='elshall@gmail.com',
            gender='Male',
            username='Elshall',
            role='patient'
        )
        self.user1=UserProfile.objects.create(
            first_name='loay',
            last_name='anwar',
            email='anwar@gmail.com',
            gender='Male',
            username='anwar',
            role='doctor'
        )
        self.patient=Patient.objects.create(user=self.user)
        self.doctor1=Doctor.objects.create(user=self.user1)
        self.appointment=Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor1
        )
        app_id=self.appointment.id
        url=reverse('seApp:PostPrescription', args=[str(app_id)])
        self.assertEquals(resolve(url).func, doctorPostPrescription)

    def test_DeletePrescription_url(self):
        self.user=UserProfile.objects.create(
            first_name='loay',
            last_name='elshall',
            email='elshall@gmail.com',
            gender='Male',
            username='Elshall',
            role='patient'
            )
        self.user1=UserProfile.objects.create(
            first_name='loay',
            last_name='anwar',
            email='anwar@gmail.com',
            gender='Male',
            username='anwar',
            role='doctor'
          )
        self.patient=Patient.objects.create(user=self.user)
        self.doctor1=Doctor.objects.create(user=self.user1)
        self.appointment=Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor1
            )
        app_id=self.appointment.id
        url=reverse('seApp:DeletePrescription', args=[str(app_id)])
        self.assertEquals(resolve(url).func, doctorDeletePrescription)

    def test_viewprescription_url(self):
        self.user=UserProfile.objects.create(
            first_name='loay',
            last_name='elshall',
            email='elshall@gmail.com',
            gender='Male',
            username='Elshall',
            role='patient'
            )
        self.user1=UserProfile.objects.create(
            first_name='loay',
            last_name='anwar',
            email='anwar@gmail.com',
            gender='Male',
            username='anwar',
            role='doctor'
          )
        self.patient=Patient.objects.create(user=self.user)
        self.doctor1=Doctor.objects.create(user=self.user1)
        self.appointment=Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor1
            )
        app_id=self.appointment.id
        url=reverse('seApp:viewprescription', args=[str(app_id)])
        self.assertEquals(resolve(url).func, viewprescription)

    def test_UserProfile_url(self):        
        self.user1=UserProfile.objects.create(
            first_name='loay',
            last_name='anwar',
            email='anwar@gmail.com',
            gender='Male',
            username='anwar',
            role='doctor'
          )
        self.doctor1 = Doctor.objects.create(user=self.user1)
        doctor_id=self.doctor1.id
        url=reverse('seApp:viewDoctor', args=[str(doctor_id)])
        self.assertEquals(resolve(url).func, viewDoctor) 
#////////////////////////////////////////////////////////////////////////////////////////////////////////////
#Testing views
class test_Views(TestCase):    
    def setUp(self):
        self.client=Client()
        self.group_doctor = Group.objects.create(name='doctor')
        self.group_staff = Group.objects.create(name='staff')
        self.group_patient = Group.objects.create(name='patient')
        self.group_admin = Group.objects.create(name='admin')
        self.user=UserProfile.objects.create(
            username='Ehab_111',
            email='ehab@gmail.com',
            first_name='Omar',
            last_name='Ehab',
            role='patient'
        )
        self.user.set_password('12345')
        self.user.groups.add(self.group_patient)        
        self.user.save()
        self.user2=UserProfile.objects.create(
            username='AmrAhmed',
            email='amr@gmail.com',
            first_name='Amr',
            last_name='Ahmed',
            role='doctor',
        )
        self.user2.set_password('12345')
        self.user2.groups.add(self.group_doctor)
        self.user2.save()

        self.user3=UserProfile.objects.create(
            username='AliSayed',
            email='Ali@gmail.com',
            first_name='Ali',
            last_name='Sayed',
            role='staff'
        )
        self.user3.set_password('12345')
        self.user3.groups.add(self.group_staff)        
        self.user3.save()

        self.patient=Patient.objects.create(user=self.user)
        self.doctor=Doctor.objects.create(user=self.user2)
        self.staff=Staff.objects.create(user=self.user3, specialization='nurse')


        self.doctor.specialization='Pediatrician'
        self.doctor.fees=200
        self.doctor.time_slots = ['2020-03-10 11:16:09.184106+01:00', '2021-03-10 11:16:09.184106+01:00', '2022-03-10 11:16:09.184106+01:00', '2023-03-10 11:16:09.184106+01:00']
        self.doctor.save()


        self.patient.medical_history=['diabetes','heart surgery']
        self.patient.save()


        self.appointment=Appointment.objects.create(patient=self.patient,doctor=self.doctor,status='Pending')
        self.appointment.prescription=['Ogmanten']
        self.appointment.save()

        
        self.appointment2 = Appointment.objects.create(patient=self.patient,doctor=self.doctor,status='Paid')
        self.appointment2.save()
        self.appointment3 = Appointment.objects.create(patient=self.patient,doctor=self.doctor,status='Done')
        self.appointment3.save()
        self.clinic=Clinic.objects.create(owner_id=self.doctor.id,name='Healthy Life')
        self.clinic.save()


        self.staff.doctor=self.doctor
        self.staff.save()

        self.doctor.clinic=self.clinic
        self.payment=Payment.objects.create(appointment=self.appointment,key='fhkbkjd6546',amount=209529)
        self.url_home=reverse('seApp:home')
        self.url_test=reverse('seApp:test')
        self.doctor.save()
        self.staff.save()
    def test_home_view(self):
        response=self.client.get(self.url_home)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'seApp/index.html')

    def test_logout_view(self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.get(reverse('seApp:logout'))
        self.client.logout()
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_appointment_view(self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.get(reverse('seApp:appointment', args=[str(self.appointment.id)]))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'seApp/appointment.html')

    def test_staffProfile(self):
        self.client.login(username='AliSayed',password='12345')
        response = self.client.get(reverse('seApp:StaffProfile'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'seApp/staffProfile.html')


    def test_appointmentGetManager(self):
        self.client.login(username='AmrAhmed',password='12345')
        response = self.client.get(reverse('seApp:appointmentGetManager'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'seApp/appointmentManager.html')


    def test_postAppointment(self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.post(reverse('seApp:postAppointment', args=[str(self.appointment.id)]), {'newTimeSlot':'0'})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/doctor/appointment/'+str(self.appointment.id), status_code=302, target_status_code=200, fetch_redirect_response=True)


    def test_deleteAppointment(self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.get(reverse('seApp:deleteAppointment', args=[str(self.appointment.id)]))
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/doctor/appointment', status_code=302, target_status_code=200, fetch_redirect_response=True)
        

    def test_appointment(self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.get(reverse('seApp:appointment', args=[str(self.appointment.id)]))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'seApp/appointment.html')


    def test_doctorPostPrescription(self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.post(reverse('seApp:PostPrescription', args=[str(self.appointment.id)]), {'newMedication':'Ogmanten'})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/doctor/appointment/'+str(self.appointment.id), status_code=302, target_status_code=200, fetch_redirect_response=True)


    def test_doctorDeletePrescription(self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.post(reverse('seApp:DeletePrescription', args=[str(self.appointment.id)]), {'deletedMedication':'Ogmanten'})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/doctor/appointment/'+str(self.appointment.id), status_code=302, target_status_code=200, fetch_redirect_response=True)


    def test_doctorGetPatients(self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.get(reverse('seApp:patients'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'seApp/patients.html')


    def test_get_doctorTransferPatient(self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.get(reverse('seApp:TransferPatients',  args=[str(self.patient.id)]))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'seApp/patientsTransfer.html')


    def test_post_doctorTransferPatient(self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.post(reverse('seApp:TransferPatients', args=[str(self.patient.id)]), {'doctor':self.doctor.id, 'timeslot':0})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/doctor/patients/', status_code=302, target_status_code=200, fetch_redirect_response=True)    
        
    def test_DoctorProfile(self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.get(reverse('seApp:DoctorProfile'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'seApp/doctorProfile.html')     
        
    def test_staffGetDetails(self):
        self.client.login(username='AliSayed',password='12345')
        response=self.client.get(reverse('seApp:staffGetDetails'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'seApp/staffSpecialization.html')                 

    def test_staffPostDetails(self):
        self.client.login(username='AliSayed',password='12345')
        response=self.client.post(reverse('seApp:staffPostDetails'), {'specialization':self.staff.specialization})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/doctor/services', status_code=302, target_status_code=200, fetch_redirect_response=True)  

    def test_StaffProfile(self):
        self.client.login(username='AliSayed',password='12345')
        response=self.client.get(reverse('seApp:StaffProfile'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'seApp/staffProfile.html')            


    def test_loginpage(self):
        response = self.client.post(reverse('seApp:loginpage'), {'username':'AmrAhmed','password':'12345'})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/doctor/services', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_collect_info (self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.get(reverse('seApp:collectedInfoAdmin'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'seApp/collectedInfoAdmin.html')
    
    def test_collect_info_doctor (self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.get(reverse('seApp:collectedInfoDoctor'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'seApp/collectedInfoDoctor.html')

    def test_servicesManager (self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.get(reverse('seApp:servicesManager'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'seApp/servicesManager.html')
        
    def test_createNewClinic (self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.post(reverse('seApp:createNewClinic'),{'clinicName':'Health','clinicAddress':'3 fisal street'})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/doctor/services', status_code=302, target_status_code=200, fetch_redirect_response=True)
    
    def test_changeFeeDoctor (self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.post(reverse('seApp:changeFeeDoctor'),{'fees':'1000'})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/doctor/services', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_changeMedicalDetailsDoctor (self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.post(reverse('seApp:changeMedicalDetailsDoctor'),{'description':'graduatee of Cairo universities','specialization':'pediatrician','medicalId':'542598'})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/doctor/services', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_deleteTimeslotDoctor (self):
        self.client.login(username='AliSayed',password='12345')
        timeslot_removed = '2020-03-10 11:16:09.184106+01:00'
        response=self.client.post(reverse('seApp:deleteTimeslotDoctor'),{'timeslot':timeslot_removed})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/doctor/services', status_code=302, target_status_code=200, fetch_redirect_response=True)
    
    def test_addTimeslotDoctor (self):
        self.client.login(username='AliSayed',password='12345')
        timeslot_removed = '2020-03-10T10:16:09'
        response=self.client.post(reverse('seApp:addTimeslotDoctor'),{'timeslot':timeslot_removed})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/doctor/services', status_code=302, target_status_code=200, fetch_redirect_response=True)
   
    def test_staffManager (self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.get(reverse('seApp:staffManager'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,  'seApp/staffManager.html')

    def test_addNewStaff (self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.post(reverse('seApp:addNewStaff'),{'staff':self.staff.id})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/doctor/staff', status_code=302, target_status_code=200, fetch_redirect_response=True)
    
    def test_removeStaff (self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.post(reverse('seApp:removeStaff'),{'staff':self.staff.id})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/doctor/staff', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_addNewDoctor (self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.post(reverse('seApp:addNewDoctor'),{'doctor':self.doctor.user.id,'clinic':self.clinic.id})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/doctor/staff', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_removeDoctor (self):
        self.client.login(username='AmrAhmed',password='12345')
        response=self.client.post(reverse('seApp:removeDoctor'),{'doctor':self.doctor.user.id})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/doctor/staff', status_code=302, target_status_code=200, fetch_redirect_response=True)
     
    def test_browse(self):
        self.client.login(username='Ehab_111',password='12345')
        response=self.client.post(reverse('seApp:browse'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,  'seApp/browse.html')

    def test_appointmentUser(self):
        self.client.login(username='Ehab_111',password='12345')
        response=self.client.post(reverse('seApp:appointmentUser'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'seApp/appointmentUser.html')
    
    def test_appointmentViewCancel(self):
        self.client.login(username='Ehab_111',password='12345')
        app_id=self.appointment2.id
        response=self.client.post(reverse('seApp:appointmentView',args=[str(app_id)]),{'cancel':True})
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'seApp/appointmentcancelled.html')

    def test_appointmentViewPaid(self):
        self.client.login(username='Ehab_111',password='12345')
        app_id=self.appointment2.id
        response=self.client.post(reverse('seApp:appointmentView',args=[str(app_id)]))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'seApp/appointmentpaid.html')

    
    def test_appointmentViewDone(self):
        self.client.login(username='Ehab_111',password='12345')
        app_id=self.appointment3.id
        response=self.client.post(reverse('seApp:appointmentView',args=[str(app_id)]),{'submit':True,'rate': 5})
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'seApp/appointmentdone.html')
    
    def test_viewprescription(self):
        self.client.login(username='Ehab_111',password='12345')
        app_id=self.appointment3.id
        response=self.client.post(reverse('seApp:viewprescription',args=[str(app_id)]))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'seApp/viewprescription.html')
    
    def test_viewDoctor(self):
        self.client.login(username='Ehab_111',password='12345')
        doctor=self.doctor.id
        response=self.client.post(reverse('seApp:viewDoctor',args=[str(doctor)]))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'seApp/viewDoctor.html')
    
    def test_emergency (self):
        self.client.login(username='Ehab_111',password='12345')
        response=self.client.post(reverse(('seApp:emergency'), args=[str(self.doctor.id)]))
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/user/appointment', status_code=302, target_status_code=200, fetch_redirect_response=True)
    
    def test_updateProfile (self):
        self.client.login(username='Ehab_111',password='12345')
        response=self.client.post(reverse('seApp:updateProfile'),{'first_name':'Ehab','last_name':'Ehabtany','email':'EhabEhab@gmail.com','phone':'011564897561','medical_history':['heart surgery','diabetes','corona']})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/user/profile', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_changePassword (self):
        self.client.login(username='Ehab_111',password='12345')
        response=self.client.post(reverse('seApp:change_password'), {'old_password':'12345','new_password1':'123456789EhaB','new_password2':'123456789EhaB'})
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/user/profile', status_code=302, target_status_code=200, fetch_redirect_response=True)
    

    def UserProfile(self):
        self.client.login(username='Ehab_111',password='12345')
        response=self.client.post(reverse('seApp:UserProfile'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'seApp/userProfile.html')
#////////////////////////////////////////////////////////////////////////////////////////////////////////////
#Testing models

class test_models(TestCase):
    def setUp(self):
        self.user=UserProfile.objects.create(
            username='Ehab_111',
            email='ehab@gmail.com',
            first_name='Omar',
            last_name='Ehab',
            role='Patient'
        )
        self.user2=UserProfile.objects.create(
            username='AmrAhmed',
            email='amr@gmail.com',
            first_name='Amr',
            last_name='Ahmed',
            role='Doctor'
        )
        self.user3=UserProfile.objects.create(
            username='AliSayed',
            email='Ali@gmail.com',
            first_name='Ali',
            last_name='Sayed',
            role='Staff'
        )
        self.patient=Patient.objects.create(user=self.user)
        self.doctor=Doctor.objects.create(user=self.user2)
        self.staff=Staff.objects.create(user=self.user3, specialization='Nurse')
        self.doctor.specialization='Pediatrician'
        self.doctor.fees=200
        self.patient.medical_history=['diabetes','heart surgery']
        self.appointment=Appointment.objects.create(patient=self.patient,doctor=self.doctor,status='Pending')
        self.clinic=Clinic.objects.create(owner_id=self.doctor.id,name='Healthy Life')
        self.staff.doctor=self.doctor
        self.payment=Payment.objects.create(appointment=self.appointment,key='fhkbkjd6546')

    def test_userprofile_model (self):
        self.assertEquals(self.user.role,'Patient')
        self.assertEquals(self.user.username,'Ehab_111')
        self.assertEquals(self.user.email, 'ehab@gmail.com')
    
    def test_Patient_model (self):
        self.assertEquals(self.patient.medical_history, ['diabetes','heart surgery'])

    def test_Doctor_model (self):
        self.assertEquals(self.doctor.specialization,'Pediatrician')
        self.assertEquals(self.doctor.user.first_name,'Amr')
    
    def test_Staff_model (self):
        self.assertEquals(self.staff.specialization,'Nurse')
        self.assertEquals(self.staff.user.username,'AliSayed')    

    def test_Clinic_model (self):
        self.assertEquals(self.clinic.name, 'Healthy Life')
        self.assertAlmostEquals(self.clinic.owner_id, self.doctor.id)

    def test_Appointment_model (self):
        self.assertEquals(self.appointment.patient.user.first_name,'Omar')
        self.assertAlmostEquals(self.appointment.doctor.fees, 200)
        self.assertAlmostEquals(self.appointment.status, 'Pending')
    
    def test_Payment_model (self):
        self.assertEquals(self.payment.key, 'fhkbkjd6546')
        self.assertAlmostEquals(self.payment.appointment.id, self.appointment.id) 
    






        





