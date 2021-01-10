from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

UserAdmin.fieldsets += ('Custom fields set', {'fields': ('phone', 'gender','birth_date','role')}),
# Register your models here.
admin.site.register(UserProfile,UserAdmin)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Payment)
admin.site.register(Clinic)
admin.site.register(Staff)
