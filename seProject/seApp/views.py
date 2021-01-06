from django.shortcuts import render, redirect
from .models import Doctor, Appointment
from .forms import PrescriptionForm

# Create your views here.
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
    services_list = {'fees':'100$', 'timeslots':[{'id':0,'slot':'2020/12/12'},{'id':1,'slot':'2020/12/12'},{'id':2,'slot':'2020/12/12'}] }
    context = {'services_list': services_list}
    return render(request, 'seApp/servicesManager.html', context)


def staffManager(request):
    staff_list = [{'id':0, 'name':'John', 'details': 'nurse'}, {'id':1, 'name':'John', 'details': 'nurse'},{'id':2, 'name':'John', 'details': 'nurse'},{'id':3, 'name':'John', 'details': 'nurse'}]
    context = {'staff_list': staff_list}
    return render(request, 'seApp/staffManager.html', context)


def browse(request):
    return render(request,'seApp/browse.html')