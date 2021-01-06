from django.forms import ModelForm
from .models import Appointment

class PrescriptionForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ('prescription',)