from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect

def unauthenticted_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            role = request.user.role
            if (role == 'patient'):
                return redirect('seApp:browse')
            elif(role == 'doctor'):
                return redirect('seApp:servicesManager')
            elif(role == 'staff'):
                return redirect('seApp:staffGetDetails')
            else:
                return redirect('seApp:collectedInfoAdmin')
        else:
            return view_func(request,*args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    allowed_roles.append('admin')
    def decorator (view_func):
        def wrapper_func(request,*args, **kwargs):
            group =None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args, **kwargs)
            else:
                return HttpResponseForbidden()
        return wrapper_func
    return decorator 
