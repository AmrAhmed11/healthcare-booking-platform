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
        self.user=UserProfile.objects.create(
            username='Ehab_111',
            email='ehab@gmail.com',
            first_name='Omar',
            last_name='Ehab',
            role='Patient'
        )
        self.user.set_password('12345')
        self.user.save()

        self.user2=UserProfile.objects.create(
            username='AmrAhmed',
            email='amr@gmail.com',
            first_name='Amr',
            last_name='Ahmed',
            role='Doctor'
        )
        self.user2.set_password('12345')
        self.user2.save()

        self.user3=UserProfile.objects.create(
            username='AliSayed',
            email='Ali@gmail.com',
            first_name='Ali',
            last_name='Sayed',
            role='staff'
        )
        self.user3.set_password('12345')
        self.user3.save()

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
        self.url_home=reverse('seApp:home')
        self.url_test=reverse('seApp:test')
    def test_home_view(self):
        response=self.client.get(self.url_home)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'seApp/index.html')
    # def test_logout_view(self):
    #     response=self.client.get(reverse('seApp:logout'))
    #     self.client.logout()
    #     self.assertEquals(response.status_code,302)
    #     self.assertEquals(response.get('seApp:home'), '/')

    # def test_appointment_view(self):
    #     self.client.login(username='AmrAhmed',password='12345')
    #     response=self.client.get(reverse('seApp:appointment', args=[str(self.appointment.id)]))
    #     self.assertEquals(response.status_code,200)
    #     self.assertTemplateUsed(response, 'seApp/appointment.html/')

    def test_staffProfile(self):
        self.client.login(username='AliSayed',password='12345')
        response = self.client.get(reverse('seApp:StaffProfile'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'seApp/staffProfile.html')

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
    






        





