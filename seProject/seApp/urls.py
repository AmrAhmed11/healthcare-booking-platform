"""seApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views

app_name = 'seApp'
urlpatterns = [
    path('',views.index,name='home'),
    path('test',views.test,name='test'),


    path('doctor/appointment', views.appointmentGetManager, name='appointmentGetManager'),
    path('doctor/appointment/<int:app_id>', views.appointment, name='appointment'),
    path('doctor/appointment/<int:app_id>/edit', views.postAppointment, name='postAppointment'),
    path('doctor/appointment/<int:app_id>/delete', views.deleteAppointment, name='deleteAppointment'),
    path('doctor/patients/', views.doctorGetPatients, name='patients'),
    path('doctor/patients/transfer/<int:patient_id>', views.doctorTransferPatient, name='TransferPatients'),
    path('doctor/patients/prescription/<int:app_id>/create', views.doctorPostPrescription, name='PostPrescription'),
    path('doctor/patients/prescription/<int:app_id>/delete', views.doctorDeletePrescription, name='DeletePrescription'),
    path('doctor/staff', views.staffManager, name='staffManager'),
    path('doctor/services', views.servicesManager, name='servicesManager'),
    path('doctor/createNewClinic', views.createNewClinic, name='createNewClinic'),
    path('doctor/deleteTimeslot', views.deleteTimeslotDoctor, name='deleteTimeslotDoctor'),
    path('doctor/addNewStaff', views.addNewStaff, name='addNewStaff'),
    path('doctor/removeStaff', views.removeStaff, name='removeStaff'),
    path('doctor/addNewDoctor', views.addNewDoctor, name='addNewDoctor'),
    path('doctor/removeDoctor', views.removeDoctor, name='removeDoctor'),
    path('doctor/addTimeslot', views.addTimeslotDoctor, name='addTimeslotDoctor'),
    path('doctor/changeMedicalDetails', views.changeMedicalDetailsDoctor, name='changeMedicalDetailsDoctor'),
    path('doctor/changeFeeDoctor', views.changeFeeDoctor, name='changeFeeDoctor'),
    path('doctor/profile', views.DoctorProfile, name="DoctorProfile"),
    path('doctor/collectedInfo', views.collectedInfoDoctor, name="collectedInfoDoctor"),


    path('admin/collectedInfo', views.collectedInfoAdmin, name="collectedInfoAdmin"),    
   

    path('staff/details/', views.staffGetDetails, name='staffGetDetails'),
    path('staff/details/select', views.staffPostDetails, name='staffPostDetails'),
    path('staff/profile', views.StaffProfile, name='StaffProfile'),
    path('user/appointment', views.appointmentUser, name='appointmentUser'),
    path('user/appointmentview/<int:app_id>', views.appointmentView, name='appointmentView'),
    path('user/appointmentview/viewprescription/<int:app_id>', views.viewprescription, name='viewprescription'),
    path('user/browse',views.browse,name='browse'),


    path('logout/',views.logout_path,name="logout"),
    path('login/',views.loginpage,name="loginpage"),
    path('register/',views.register,name="register"),
    path('user/view-doctor/<int:doctor_id>', views.viewDoctor, name='viewDoctor'),
    path('user/profile', views.UserProfile, name="UserProfile"),

    path('complete/<int:doctor_id>', views.paymentComplete, name="complete"),
    # path('user/edit-profile', views.editProfile, name="editProfile"),

    # path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/change_password', views.changePassword, name="change_password"),
    path('user/update-profile', views.updateProfile, name="updateProfile"),
    path('emergency/<int:doctor_id>',views.emergency,name='emergency')
]
