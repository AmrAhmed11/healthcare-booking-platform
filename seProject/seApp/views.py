from django.shortcuts import render
# from .models import Doctor

# Create your views here.
def index(request):
    
    return render(request, 'seApp/index.html')


def appointmentManager(request):
    app_list = [{'id':0, 'date':'1/1/2022', 'state': 'Pending'}, {'id':1, 'date':'1/2/2022', 'state': 'Pending'}, {'id':2, 'date':'1/1/2022', 'state': 'Pending'}, {'id':3, 'date':'1/2/2022', 'state': 'Pending'}]
    context = {'app_list': app_list}
    return render(request, 'seApp/appointmentManager.html', context)

def appointment(request, app_id):
    app = {'id':4, 'date':'1/1/2022', 'state': 'Pending'}
    context = {'app': app}
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