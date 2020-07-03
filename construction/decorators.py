from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group == "Client":
                return redirect('client_home')
            elif group == "Project Manager":
                return redirect('project_list_pm')
            elif group == "Person In-Charge":
                return redirect('project_list_pic')
            elif group == "Warehouseman":
                return redirect('requisition_list_whm')
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

def pm_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group =='Project Manager':
            return view_func(request, *args, **kwargs)
        else:
            return render(request, '403.html')
    return wrapper_func    

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group =='Admin':
            return view_func(request, *args, **kwargs)
        else:
            return render(request, "403.html")
    return wrapper_func    

def pic_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group =='Person In-Charge':
            return view_func(request, *args, **kwargs)
        else:
            return render(request, "403.html")
    return wrapper_func 

def whm_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group =='Warehouseman':
            return view_func(request, *args, **kwargs)
        else:
            return render(request, "403.html")
    return wrapper_func    

def client_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group =='Client':
            return view_func(request, *args, **kwargs)
        else:
            return render(request, "403.html")
    return wrapper_func    

def no_whm(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group !='Warehouseman':
            return view_func(request, *args, **kwargs)
        else:
            return render(request, "403.html")
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
                return render(request, "403.html")
        return wrapper_func
    return decorator


