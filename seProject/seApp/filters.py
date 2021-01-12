import django_filters 
from . models import * 
from django_filters import NumberFilter, CharFilter

class DoctorFilter(django_filters.FilterSet):
    
    user__first_name = CharFilter(field_name="user__first_name", lookup_expr='icontains')
    user__last_name = CharFilter(field_name="user__last_name", lookup_expr='icontains')
    specialization = CharFilter(field_name="specialization", lookup_expr='icontains')
    clinic__name = CharFilter(field_name="clinic__name", lookup_expr='icontains')
    clinic__address = CharFilter(field_name="clinic__address", lookup_expr='icontains')
    fees = NumberFilter(field_name="fees", lookup_expr='lte')
    
    class Meta :
        model = Doctor 
        exclude = ['fees','time_slots','user','clinic','specialization','rating','medical_id','description']
