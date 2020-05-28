from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group == "Client":
                return redirect('client_home')
            else:
                return redirect('project_list')
        else:    
            return view_func(request, *args, **kwargs)

    return wrapper_func

def staff_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group =='Client':
            return redirect('client_home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func    

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
                
            elif group == 'Client':
                return redirect('client_home')
            else:
                return HttpResponse("You cannot view this page")
        return wrapper_func
    return decorator


def level_4(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if group =='Client':
            return redirect('client_home')
        if group =='Admin':
           return view_func(request, *args, **kwargs)
    return wrapper_function

