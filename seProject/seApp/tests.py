from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse
from .views import *
from .models import *
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
        self.doctor1=Doctor.objects.create(user=self.user1)
        doctor_id=self.doctor1.id
        url=reverse('seApp:viewDoctor', args=[str(doctor_id)])
        self.assertEquals(resolve(url).func, viewDoctor) 





