from django.shortcuts import render
# from .models import Doctor

# Create your views here.
def appointmentManager(request):
    app_list = [{'id':0, 'date':'1/1/2022', 'state': 'Pending'}, {'id':1, 'date':'1/2/2022', 'state': 'Pending'}, {'id':2, 'date':'1/1/2022', 'state': 'Pending'}, {'id':3, 'date':'1/2/2022', 'state': 'Pending'}]
    context = {'app_list': app_list}
    return render(request, 'seApp/appointmentManager.html', context)

def appointment(request, app_id):
    app = {'id':4, 'date':'1/1/2022', 'state': 'Pending'}
    context = {'app': app}
    return render(request, 'seApp/appointment.html', context)
