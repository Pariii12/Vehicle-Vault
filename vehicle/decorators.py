from django.shortcuts import redirect,HttpResponse 
from django.conf import settings

def role_required(allowed_roles=[]):
    def decorator(view_func): #adminDashboardView
        def wrapper_func(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(settings.LOGIN_URL)
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page")
        return wrapper_func
    return decorator




