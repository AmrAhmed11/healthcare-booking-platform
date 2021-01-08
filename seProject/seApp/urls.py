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
from django.urls import path
from . import views

app_name = 'seApp'
urlpatterns = [
    path('',views.index,name='home'),
    path('doctor/appointment', views.appointmentManager, name='appointmentManager'),
    path('doctor/appointment/<int:app_id>', views.appointment, name='appointment'),
    path('doctor/staff', views.staffManager, name='staffManager'),
    path('doctor/services', views.servicesManager, name='servicesManager'),
    path('doctor/deleteTimeslot', views.deleteTimeslotDoctor, name='deleteTimeslotDoctor'),
    path('doctor/addNewStaff', views.addNewStaff, name='addNewStaff'),
    path('doctor/removeStaff', views.removeStaff, name='removeStaff'),
    path('doctor/addTimeslot', views.addTimeslotDoctor, name='addTimeslotDoctor'),
    path('doctor/changeFeeDoctor', views.changeFeeDoctor, name='changeFeeDoctor'),
    path('user/appointment/<int:app_id>', views.appointmentUser, name='appointment'),
    path('user/browse',views.browse,name='browse'),
    path('logout/',views.logoutuser,name="logout"),
    path('login/',views.loginpage,name="loginpage"),
    path('register/',views.register,name="register"),
    path('user/view-doctor/<int:doctor_id>', views.viewDoctor, name='viewDoctor'),
]
