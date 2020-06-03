from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from Poliworks.settings import EMAIL_HOST_USER
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import *
from django.views.generic import *
from .decorators import *
from .forms import *
from .models import *
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import *


def home(request):
    return render(request, 'frontend/landingpage.html')

def about(request):
    return render(request, 'frontend/about.html')
    
@unauthenticated_user
def signin(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            group = request.user.groups.all()[0].name
            if group == 'Client':
                return redirect('client_home')
            elif group == "Project Manager":
                return redirect('project_list_pm')
            elif group == "Person In-Charge":
                return redirect('project_list_pic')
            elif group == "Warehouseman":
                return redirect('requisition_create')
            else:
                return redirect('project_list')
        else:
            messages.warning(request, 'Email or Password is incorrect', extra_tags="danger")
    return render(request, 'frontend/signin.html')

def signout(request):
    logout(request)
    return redirect('signin')

#################################################################################################################################
#################################################################################################################################
@login_required(login_url='signin')
@allowed_users(allowed_roles=['Admin'])
def signupclient(request):
    if request.method=='POST':
        user = SignupFormClient(request.POST)
        profile = ProfileForm(request.POST)
        if user.is_valid() and profile.is_valid():
            user = user.save()
            profile = profile.save(False)
            profile.user = user
            profile.save()
        account = User.objects.get(id = profile.user.id)
        password_form = PasswordResetForm({'email':account.email})
        if password_form.is_valid():
            password_form.save(request= request, email_template_name='email/welcome.html', subject_template_name='email/welcome_subject.txt')
            messages.success(request,'Client account has been created', extra_tags="success")
            return redirect('signupclient')
    else:
        user = SignupFormClient()
        profile = ProfileForm()
    context = {'user':user,'profile':profile,}
    return render(request, 'backoffice/account_pages/signup_client.html', context)

@login_required(login_url='signin')
@allowed_users(allowed_roles=['Admin'])
def signupwhm(request):
    if request.method=='POST':
        user = SignupFormWHM(request.POST)
        profile = ProfileForm(request.POST)
        if user.is_valid() and profile.is_valid():
            user=user.save()
            profile=profile.save(False)
            profile.user=user
            profile.save()
            messages.success(request, 'Warehouseman account created successfully', extra_tags='success')
            return redirect('signupwhm')
    else:
        user = SignupFormWHM()
        profile = ProfileForm()
    context = {'user':user,'profile':profile,}
    return render(request, 'backoffice/account_pages/signup_whm.html', context)

@login_required(login_url='signin')
@allowed_users(allowed_roles=['Admin'])
def signuppic(request):
    if request.method=='POST':
        user = SignupFormPIC(request.POST)
        profile = ProfileForm(request.POST)
        if user.is_valid() and profile.is_valid():
            user=user.save()
            profile=profile.save(False)
            profile.user=user
            profile.save()
            messages.success(request,'Person In-Charge account created successfully',extra_tags="success")
            return redirect('signuppic')
    else:
        user = SignupFormPIC()
        profile = ProfileForm()
    context = {'user':user,'profile':profile,}
    return render(request, 'backoffice/account_pages/signup_pic.html', context)

@login_required(login_url='signin')
@allowed_users(allowed_roles=['Admin'])
def signuppm(request):
    if request.method=='POST':
        user = SignupFormPM(request.POST)
        profile = ProfileForm(request.POST)
        if user.is_valid() and profile.is_valid():
            user=user.save()
            profile=profile.save(False)
            profile.user=user
            profile.save()
            messages.success(request,'Project Manager account created successfully', extra_tags="success")
            return redirect('signuppm')
    else:
        user = SignupFormPM()
        profile = ProfileForm()
    context = {'user':user,'profile':profile,}
    return render(request, 'backoffice/account_pages/signup_pm.html', context)

@login_required(login_url='signin')
@staff_only
def profile(request):
    form=ProfileForm
    context={'form':form}
    return render(request, 'backoffice/account_pages/profile.html', context)

@login_required(login_url='signin')
@staff_only
def editprofile(request):
    user = request.user
    profile = request.user.profile
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        user_form = UserEditForm(request.POST, instance=user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ' Your Profile has been updated', extra_tags="success")
            return redirect('userprofile')
    else:
        user_form = UserEditForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)
    context={'profile_form':profile_form,'user_form':user_form}
    return render(request, 'backoffice/account_pages/updateprofile.html', context)

@login_required(login_url='signin')
def ChangePasswordView(request):
    form = PasswordChangeForm(user=request.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        messages.success(request, "Password has been changed!", extra_tags="success")
        return redirect('userprofile')
    context={'form':form,}
    return render(request, 'backoffice/account_pages/change_password.html', context)


#################################################################################################################################
#################################################################################################################################
@login_required(login_url='signin')
@allowed_users(allowed_roles=['Admin','Project Manager'])
def ProjectCreateView(request):
    form = ProjectForm
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project has been created!', extra_tags="success")
            return redirect('project_list')
        else:
            messages.info(request, 'Failed on Creating Project', extra_tags="warning")
            return redirect('project_create')
    context = {'form':form}
    return render(request, 'backoffice/project_pages/project_create.html', context)

@login_required(login_url='signin')
@allowed_users(allowed_roles=['Admin','Project Manager'])
def ProjectUpdateView(request,pk):
    data = ProjectSite.objects.get(id=pk)
    if request.method == 'POST':
        form = ProjectUpdateForm(request.POST,instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project Details has been updated!', extra_tags="success")
            return redirect('project_detail', pk=data.id)
        else:
            messages.warning(request, 'Failed to update Project', extra_tags="warning")
    else:
        form = ProjectUpdateForm(instance=data)
    context = {'form':form, 'data':data}
    return render(request, 'backoffice/project_pages/project_update.html', context)

@login_required(login_url='signin')
@admin_only
def ProjectListView(request):
    data = ProjectSite.objects.all()
    data2 = ProjectSite.objects.filter(status="Completed")
    data3 = ProjectSite.objects.filter(status="On-going")
    data4 = ProjectSite.objects.filter(status="Pending")
    completed = data2.count()
    ongoing = data3.count()
    pending = data4.count()
    context={'data':data, 'completed':completed, 'ongoing':ongoing, 'pending':pending}
    return render(request,'backoffice/project_pages/project_list.html', context)

@login_required(login_url='signin')
@pm_only
def ProjectListView_PM(request):
    data = ProjectSite.objects.filter(pm=request.user)
    data2 = ProjectSite.objects.filter(status="Completed")
    data3 = ProjectSite.objects.filter(status="On-going")
    data4 = ProjectSite.objects.filter(status="Pending")
    completed = data2.count()
    ongoing = data3.count()
    pending = data4.count()
    context={'data':data, 'completed':completed, 'ongoing':ongoing, 'pending':pending}
    return render(request,'backoffice/project_pages/project_list.html', context)

@login_required(login_url='signin')
@pic_only
def ProjectListView_PIC(request):
    data = ProjectSite.objects.filter(pic=request.user)
    data2 = ProjectSite.objects.filter(status="Completed")
    data3 = ProjectSite.objects.filter(status="On-going")
    data4 = ProjectSite.objects.filter(status="Pending")
    completed = data2.count()
    ongoing = data3.count()
    pending = data4.count()
    context={'data':data, 'completed':completed, 'ongoing':ongoing, 'pending':pending}
    return render(request,'backoffice/project_pages/project_list.html', context)

@login_required(login_url='signin')
@staff_only
def ProjectDetailView(request, pk):
    data = ProjectSite.objects.get(id=pk)
    data2 = Quotation.objects.filter(projectsite_id=data.id)
    try:
        data3 = ProjectProgress.objects.get(projectsite_id=data.id)
        data4 = ProjectProgressDetails.objects.filter(projectprogress=data3.id)
    except ObjectDoesNotExist:
        context={'data':data, 'data2':data2}
        return render(request, 'backoffice/project_pages/project_detail.html', context)
    context={'data':data, 'data2':data2,'data3':data3,'data4':data4,}
    return render(request, 'backoffice/project_pages/project_detail.html', context)

@login_required(login_url='signin')
@staff_only
def ProjectDetailView_PIC(request, pk):
    data = ProjectSite.objects.get(id=pk)
    data2 = Quotation.objects.filter(projectsite_id=data.id)
    try:
        data3 = ProjectProgress.objects.get(projectsite_id=data.id)
        data4 = ProjectProgressDetails.objects.filter(projectprogress=data3.id)
    except ObjectDoesNotExist:
        context={'data':data, 'data2':data2}
        return render(request, 'backoffice/project_pages/project_detail.html', context)
    context={'data':data, 'data2':data2,'data3':data3,'data4':data4,}
    return render(request, 'backoffice/project_pages/project_detail.html', context)

#################################################################################################################################
#################################################################################################################################
class QuotationCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url ="signin"
    redirect_field_name="redirect_to"
    model=Quotation
    fields=('projectsite','subject','date',)
    template_name ='backoffice/quotation_pages/quotation_create.html'
    success_message = "Quotation has been created"
    
    @method_decorator(staff_only, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super(QuotationCreateView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["formset"] = QuotationFormSet(self.request.POST)
        else:
            data["formset"] = QuotationFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            quotation = self.object
            quotation.amount = 0
            quotation_list = formset.save()
            for i in quotation_list:
                quotation.amount += i.unitcost()
            quotation.save()
            return super(QuotationCreateView, self).form_valid(form)
        
    def get_success_url(self):
        data = self.object
        data2 = data.projectsite.id
        return reverse_lazy("project_detail", kwargs={'pk': data2})

class QuotationUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url ="signin"
    redirect_field_name = "redirect_to"
    model = Quotation
    fields = ('subject',)
    template_name = 'backoffice/quotation_pages/quotation_update.html'
    success_message = "Quotation has been updated"
    
    @method_decorator(staff_only, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super(QuotationUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(QuotationUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data["formset"] = QuotationUpdateFormSet(self.request.POST, instance=self.object)
        else:
            data["formset"] = QuotationUpdateFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            data2 = self.object
            data3 = QuotationDetails.objects.filter(quotation=data2.id)
            data2.amount = 0
            for i in data3:
                data2.amount +=i.unitcost()
            data2.save()
            return super(QuotationUpdateView, self).form_valid(form)
        
    def get_success_url(self):
        data=self.kwargs['pk']
        return reverse_lazy("quotation_detail", kwargs={'pk': data})

@login_required(login_url='signin')
@allowed_users(allowed_roles=['Admin'])
def QuotationListView(request):
    data = Quotation.objects.all().order_by('date')
    data2 = QuotationDetails.objects.all()
    context={'data':data ,'data2':data2}
    return render(request, 'backoffice/quotation_pages/quotation_list.html', context)

@login_required(login_url='signin')
@allowed_users(allowed_roles=['Admin','Project Manager'])
def QuotationDetailView(request,pk):
    data = Quotation.objects.get(id=pk)
    project = ProjectSite.objects.get(id=data.projectsite.id)
    data2 = QuotationDetails.objects.filter(quotation=data.id)
    if request.method == "POST":
        try:
            data3 = ProjectProgress.objects.get(projectsite=data.projectsite.id)
            messages.warning(request, "There is an existing Work Progress. Please delete the previous one to create a new Work Progress", extra_tags="warning")
            return redirect('quotation_detail',pk=data.id)
        except ObjectDoesNotExist:
            data3 = ProjectProgress.objects.create(projectsite=data.projectsite) 
            data3.quotation = data.id
            data3.save()
            for i in data2:
                data4 = ProjectProgressDetails.objects.create(projectprogress=data3)
                scope = ScopeOfWork.objects.get(scope=i.scope_of_work.scope)
                data4.scope_of_work = scope.scope
                data4.save()
            data4.save()
            project.status = "On-going"
            project.save()
            messages.success(request, "Work Progress has been created!", extra_tags="success")
            return redirect('project_detail',pk=project.id)
    context = { 'data':data, 'data2':data2 }
    return render(request, 'backoffice/quotation_pages/quotation_detail.html', context)

@login_required(login_url='signin')
@allowed_users(allowed_roles=['Admin','Project Manager'])
def QuotationDeleteView(request,pk):
    data = Quotation.objects.get(id=pk)
    data2 = QuotationDetails.objects.filter(quotation=data.id)
    if request.method == 'POST':
        data.delete()
        messages.success(request, 'Quotion has been deleted!', extra_tags='success')
        # if request.user.groups.all()[0].name=="Project Manager":
        return redirect('project_detail', pk=data.projectsite.id)
        # else:
        #     return redirect('quotation_list')
    context={'data':data,'data2':data2,}
    return render(request, 'backoffice/quotation_pages/quotation_delete.html', context)

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Project Manager'])
def ProgressUpdateView(request,pk):
    data = ProjectProgress.objects.get(id=pk)
    data2 = ProjectProgressDetails.objects.filter(projectprogress=data.id)
    data3 = ProjectSite.objects.get(projectsite=data.projectsite)
    formset = ProgressFormset()
    divisor = 0
    dividend = 0
    if request.method == 'POST':
        formset = ProgressFormset(request.POST, instance=data)
        if formset.is_valid(): 
            formset.save()
            for i in data2:
                divisor+=i.level
                if i.status == "Done":
                    dividend+=i.level
            percentage = (dividend/divisor)*100
            data.total_progress = percentage
            data.save()
            if data.total_progress == 100:
                data3.status = "Completed"
                data3.save()
                messages.success(request,"Progress has been updated!", extra_tags="success")
                return redirect('project_detail', pk=data3.id)
            else:
                data3.status = "On-going"
                data3.save()
                messages.success(request,"Progress has been updated!")
                return redirect('project_detail', pk=data3.id)
    else:
        formset = ProgressFormset(instance=data)
    context={'formset':formset, 'data':data, 'data2':data2,}
    return render(request, 'backoffice/project_pages/progress_update.html', context)

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Project Manager'])
def ProgressDeleteView(request,pk):
    data = ProjectProgress.objects.get(id=pk)
    data2 = ProjectProgressDetails.objects.filter(projectprogress=data.id)
    data3 = ProjectSite.objects.get(projectsite=data.projectsite)
    formset = ProgressFormset()
    if request.method == "POST":
        data.delete()
        data3.status ="Pending"
        data3.save()
        messages.success(request, "Work Progress has been deleted", extra_tags="success")
        return redirect('project_detail', pk=data3.id)
    else:
        formset = ProgressFormset(instance=data)
    
    context={'formset':formset, 'data':data, 'data2':data2,}
    return render(request, 'backoffice/project_pages/progress_delete.html', context)

#################################################################################################################################
#################################################################################################################################
class RequisitionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url ="signin"
    redirect_field_name = "redirect_to"
    model = Requisition
    fields = ('projectsite','date','admin','whm')
    template_name = 'backoffice/requisition_pages/requisition_create.html'
    success_message = "Requisition has been created"

    @method_decorator(staff_only, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super(RequisitionCreateView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["formset"] = RequisitionFormSet(self.request.POST)
        else:
            data["formset"] = RequisitionFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            return super(RequisitionCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("requisition_list")

class RequisitionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url ="signin"
    redirect_field_name = "redirect_to"
    model = Requisition
    fields = ('projectsite','date','admin','whm')
    template_name = 'backoffice/requisition_pages/requisition_update.html'
    success_message = "Requisition has been updated"

    @method_decorator(staff_only, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super(RequisitionUpdateView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["formset"] = RequisitionUpdateFormSet(self.request.POST, instance=self.object)
        else:
            data["formset"] = RequisitionUpdateFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            return super(RequisitionUpdateView, self).form_valid(form)

    def get_success_url(self):
        data=self.kwargs['pk']
        return reverse_lazy("requisition_detail", kwargs={'pk': data})

@login_required(login_url='signin')
@allowed_users(allowed_roles=['Admin','Warehouseman'])
def RequisitionListView(request):
    data = Requisition.objects.all().order_by('date')
    data2 = RequisitionDetails.objects.all()
    context = {'data':data,'data2':data2}
    return render(request, 'backoffice/requisition_pages/requisition_list.html',context)

@login_required(login_url='signin')
@allowed_users(allowed_roles=['Admin','Warehouseman'])
def RequisitionDetailView(request, pk):
    data = Requisition.objects.get(id=pk)
    data2 = RequisitionDetails.objects.filter(requisition=data.id)

    context= {'data':data, 'data2':data2,}
    return render(request, 'backoffice/requisition_pages/requisition_detail.html', context)

@login_required(login_url='signin')
@allowed_users(allowed_roles=['Admin','Warehouseman'])
def RequisitionDeleteView(request, pk):
    data = Requisition.objects.get(id=pk)
    data2 = RequisitionDetails.objects.filter(requisition=data.id)
    if request.method == 'POST':
        data.delete()
        messages.success(request, 'Requisition has been deleted!', extra_tags='success')
        return redirect("requisition_list")

    context= {'data':data, 'data2':data2,}
    return render(request, 'backoffice/requisition_pages/requisition_delete.html', context)

#################################################################################################################################
#################################################################################################################################
class ExternalOrderCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url ="signin"
    redirect_field_name = "redirect_to"
    model = ExternalOrder
    fields = ('projectsite','supplier','date','whm')
    template_name ='backoffice/externalorder_pages/externalorder_create.html'
    success_message = "External Order has been updated!"

    @method_decorator(staff_only, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super(ExternalOrderCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["formset"] = ExternalOrderFormSet(self.request.POST)
        else:
            data["formset"] = ExternalOrderFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            externalorder = self.object
            externalorder.amount = 0
            externalorderdetail = formset.save()
            for i in externalorderdetail:
                externalorder.amount += i.get_total()
            externalorder.save()
            return super(ExternalOrderCreateView, self).form_valid(form)
        else:
            print(form.errors)

    def get_success_url(self):
        return reverse_lazy("externalorder_list")

class ExternalOrderUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url ="signin"
    redirect_field_name = "redirect_to"
    model = ExternalOrder
    fields = ('projectsite','supplier','date','whm')
    exclude = ['totalprice']
    template_name ='backoffice/externalorder_pages/externalorder_update.html'
    success_message = "External Order has been updated!"

    @method_decorator(staff_only, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super(ExternalOrderUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["formset"] = ExternalOrderUpdateFormSet(self.request.POST, instance=self.object)
        else:
            data["formset"] = ExternalOrderUpdateFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            data2 = self.object
            data3 = ExternalOrderDetails.objects.filter(externalorder=data2.id)
            data2.amount = 0
            for i in data3:
                data2.amount += i.get_total()
            data2.save()
            return super(ExternalOrderUpdateView, self).form_valid(form)

    def get_success_url(self):
        data=self.kwargs['pk']
        return reverse_lazy("externalorder_detail", kwargs={'pk': data})

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Warehouseman'])
def ExternalOrderListView(request):
    data = ExternalOrder.objects.all().order_by('date')
    data2 = ExternalOrderDetails.objects.all()
    context = {'data':data,'data2':data2,}
    return render(request, 'backoffice/externalorder_pages/externalorder_list.html', context)

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Warehouseman'])
def ExternalOrderDetailView(request,pk):
    data = ExternalOrder.objects.get(id=pk)
    data2 = ExternalOrderDetails.objects.filter(externalorder=data.id)
    context = {'data':data,'data2':data2,}
    return render(request, 'backoffice/externalorder_pages/externalorder_detail.html', context)

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Warehouseman'])
def ExternalOrderDeleteView(request,pk):
    data = ExternalOrder.objects.get(id=pk)
    data2 = ExternalOrderDetails.objects.filter(externalorder=data.id)
    if request.method == 'POST':
        data.delete()
        messages.success(request, 'External Order has been deleted!', extra_tags='success')
        return redirect("externalorder_list")
    context = {'data':data,'data2':data2,}
    return render(request, 'backoffice/externalorder_pages/externalorder_delete.html', context)

#################################################################################################################################
#################################################################################################################################
class JobOrderCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url ="signin"
    redirect_field_name = "redirect_to"
    model = JobOrder
    fields = ('projectsite', 'date', 'duration', 'pic', 'whm')
    template_name ='backoffice/joborder_pages/joborder_create.html'
    success_message = "Job Order has been created"
    
    @method_decorator(staff_only, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super(JobOrderCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["formset"] = JobOrderFormSet(self.request.POST)
        else:
            data["formset"] = JobOrderFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            return super(JobOrderCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("joborder_list")

class JobOrderUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url ="signin"
    redirect_field_name = "redirect_to"
    model = JobOrder
    fields = '__all__'
    template_name ='backoffice/joborder_pages/joborder_update.html'
    success_message = "Job Order has been updated!"
    
    @method_decorator(staff_only, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super(JobOrderUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["formset"] = JobOrderUpdateFormSet(self.request.POST, instance=self.object)
        else:
            data["formset"] = JobOrderUpdateFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            return super(JobOrderUpdateView, self).form_valid(form)

    def get_success_url(self):
        data=self.kwargs['pk']
        return reverse_lazy("joborder_detail", kwargs={'pk': data})

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Project Manager','Person In-Charge'])
def JobOrderListView(request):
    data = JobOrder.objects.all().order_by('date')
    data2 = JobOrderTask.objects.all()
    context = {'data':data, 'data2':data2}
    return render(request, 'backoffice/joborder_pages/joborder_list.html', context)

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Project Manager','Person In-Charge'])
def JobOrderDetailView(request,pk):
    data = JobOrder.objects.get(id=pk)
    data2 = JobOrderTask.objects.filter(joborder=data.id)
    context = {'data':data,'data2':data2}
    return render(request, 'backoffice/joborder_pages/joborder_detail.html', context)

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Project Manager','Person In-Charge'])
def JobOrderDeleteView(request,pk):
    data = JobOrder.objects.get(id=pk)
    data2 = JobOrderTask.objects.filter(joborder=data.id)
    if request.method == 'POST':
        data.delete()
        messages.success(request, 'Job Order has been deleted!', extra_tags='success')
        return redirect("joborder_list")
    context = {'data':data,'data2':data2}
    return render(request, 'backoffice/joborder_pages/joborder_delete.html', context)

#################################################################################################################################
#################################################################################################################################
@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Project Manager', 'Person In-Charge'])
def ReworkCreateView(request):
    if request.method == 'POST':
        form = ReworkForm(request.POST)
        if form.is_valid :
            form.save()
            messages.success(request, 'Rework Form has been created!')
            return redirect('rework_list')
    else:
        form = ReworkForm
    context = {'form':form}
    return render(request, 'backoffice/rework_pages/rework_create.html', context) 

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Project Manager', 'Person In-Charge'])
def ReworkUpdateView(request,pk):
    rework = Rework.objects.get(id=pk)
    if request.method == 'POST':
        form = ReworkForm(request.POST, instance=rework)
        if form.is_valid :
            form.save()
            messages.success(request, 'Rework Form has been updated!', extra_tags="success")
            return redirect('rework_list')
    else:
        form = ReworkForm(instance=rework)
    context = {'form':form}
    return render(request, 'backoffice/rework_pages/rework_update.html', context) 


@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Project Manager', 'Person In-Charge'])
def ReworkListView(request):
    data = Rework.objects.all()
    context={'data':data}
    return render(request, 'backoffice/rework_pages/rework_list.html', context) 

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Project Manager', 'Person In-Charge'])
def ReworkListView_PM(request):
    data = Rework.objects.filter(pm=request.user)
    context={'data':data}
    return render(request, 'backoffice/rework_pages/rework_list.html', context) 

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Project Manager', 'Person In-Charge'])
def ReworkDetailView(request,pk):
    data = Rework.objects.get(id=pk)
    context={'data':data}
    return render(request, 'backoffice/rework_pages/rework_detail.html', context)

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Project Manager', 'Person In-Charge'])
def ReworkDeleteView(request, pk):
    data = Rework.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        messages.success(request, 'External Order has been deleted!', extra_tags='success')
        return redirect('rework_list')
    context={'data':data}
    return render(request, 'backoffice/rework_pages/rework_delete.html', context) 

#################################################################################################################################
#################################################################################################################################
@login_required(login_url='signin')
@allowed_users(allowed_roles = ['Admin','Warehouseman'])
def projectissues(request):
    form = ProblemForm
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'form submitted!')
            return redirect('issues')
        else:
            messages.warning(request, 'Error!')
    context = {'form':form}
    return render(request, 'backoffice/report_pages/projectissues.html', context)

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Warehouseman'])
def dailyreport(request):
    form = DailyReportForm()
    if request.method == 'POST':
        form = DailyReportForm(request .POST, request.FILES)
        files = request.FILES.getlist('image')
        if form.is_valid():
            post = form.save(commit=False)
            for f in files:
                report = DailyReportForm(projectsite=post.projectsite, image=f)
                report.save()
            return redirect('dailyreport')
    context={'form':form}
    return render(request, 'backoffice/report_pages/dailyreport.html', context)

#################################################################################################################################
#################################################################################################################################
@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Client'])
def Client_home(request):
    client = request.user.id
    data = ProjectSite.objects.filter(client=client)
    context = {'data':data}
    return render(request, 'client/client-home.html', context)

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Client'])
def ClientProjectView(request,pk):
    data = ProjectSite.objects.get(id=pk)
    data2 = Quotation.objects.filter(projectsite_id=data.id)
    try:
        data3 = ProjectProgress.objects.get(projectsite_id=data.id)
        data4 = ProjectProgressDetails.objects.filter(projectprogress=data3.id)
    except ObjectDoesNotExist:
        context = {'data':data, 'data2':data2}
        return render(request, 'client/client-view_project.html', context)
    context={'data':data, 'data2':data2, 'data3':data3, 'data4':data4,}
    return render(request, 'client/client-view_project.html', context)
    
@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Client'])
def ClientQuotationView(request,pk):
    data = Quotation.objects.get(id=pk)
    project = ProjectSite.objects.get(id=data.projectsite.id)
    if project.client != request.user:
        return redirect('client_quotation')
    data2 = QuotationDetails.objects.filter(quotation=data.id)
    if request.method == "POST":
        data.status = request.POST.get("status")
        data.save()
        return redirect('client_home')
    context = {'data':data, 'data2':data2,}
    return render(request, 'client/client-quotation.html', context)

@login_required(login_url='signin')
@allowed_users(allowed_roles = ['Client'])
def ClientProfileView(request):
    form=ProfileForm
    context={'form':form}
    return render(request, 'client/client-profile.html', context)

@login_required(login_url='signin')
@allowed_users(allowed_roles = ['Client'])
def ClientProfileUpdateView(request):
    user = request.user
    profile = request.user.profile
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        user_form = UserEditForm(request.POST, instance=user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.info(request, ' Your Profile has been updated')
            return redirect('client_profile')
    else:
        user_form = UserEditForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)
    context={'profile_form':profile_form,'user_form':user_form}
    return render(request, 'client/client-profile_update.html', context)

@login_required(login_url='signin')
@allowed_users(allowed_roles = ['Client'])
def ClientChangePasswordView(request):
    form = PasswordChangeForm(user=request.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        messages.success(request, "Password has been changed!", extra_tags="success")
        return redirect('client_profile')
    context={'form':form,}
    return render(request, 'client/client-change_password.html', context)

#################################################################################################################################
#################################################################################################################################
@login_required(login_url = 'signin')
@api_view(['GET'])
def ScopeOfWorks_api(request):
    scope_of_work = ScopeOfWork.objects.all()
    serializer = ScopeOfWorkSerializer(scope_of_work, many=True)
    return Response(serializer.data)

@login_required(login_url = 'signin')
@api_view(['GET'])
def ScopeOfWork_api(request, pk):
    scope_of_work = ScopeOfWork.objects.filter(id=pk)
    serializer = ScopeOfWorkSerializer(scope_of_work, many=True)
    return Response(serializer.data)

login_required(login_url = 'signin')
@api_view(['GET'])
def Inventory_api(request, pk):
    description = Inventory.objects.filter(id=pk)
    serializer = InventorySerializer(description, many=True)
    return Response(serializer.data)

login_required(login_url = 'signin')
@api_view(['GET'])
def City_api(request,pk):
    city = City.objects.filter(province=pk)
    serializers = CitySerializers(city, many=True)
    return Response(serializers.data)