from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import *
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from Poliworks.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db.models import Q
from django.views.generic import *
from .decorators import *
from .forms import *
from .models import *
import json

from datetime import datetime
import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import *

from django.db.models import Max

def home(request):
    medical = LandingPageImage.objects.filter(title__category__name="Medical")
    residential = LandingPageImage.objects.filter(title__category__name="Residential")
    office = LandingPageImage.objects.filter(title__category__name="Office Area")
    commercial = LandingPageImage.objects.filter(title__category__name="Commercial")
    context = {'medical':medical, 'commercial':commercial, 'office':office, 'residential':residential}
    return render(request, 'frontend/landingpage.html', context)

def about(request):
    return render(request, 'frontend/about.html')

def EstimateCreateView(request):
    if request.method == 'POST':
        form = EstimateForm(request.POST)
        form2 = EstimateForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        if form.is_valid() and form2.is_valid():
            estimate = form.save()
            form2 = form2.save(False)
            for f in files:
                image = EstimateImage(estimate=estimate, image=f)
                image.save()
            messages.success(request, "Your form has been submitted. We'll be in touch soon")
            return redirect('estimate_create')
    else:
        form = EstimateForm()
        form2 = EstimateImageForm()
    context = {'form':form, 'form2':form2}
    return render(request, 'frontend/estimate.html', context)

def my_custom_page_not_found_view(request, exception):
    return render(request, "404.html")

def my_custom_error_view(request):
    return render(request, "500.html")

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
            messages.warning(request, 'Email or Password is incorrect.')
    return render(request, 'frontend/signin.html')

def signout(request):
    logout(request)
    return redirect('signin')

#################################################################################################################################
#################################################################################################################################
@login_required(login_url='signin')
@allowed_users(allowed_roles=['Admin'])
def SignupView(request):
    if request.method == 'POST':
        user = SignupForm(request.POST)
        profile = ProfileForm(request.POST)
        role = request.POST.get('account')
        if user.is_valid() and profile.is_valid():
            user = user.save()
            profile = profile.save(False)
            profile.user = user
            profile.save()
            group = Group.objects.get(id=role)
            group.user_set.add(user) 
            account = User.objects.get(id = profile.user.id)
            password_form = PasswordResetForm({'email':account.email})
            if password_form.is_valid():
                password_form.save(request= request, email_template_name='email/welcome.html', subject_template_name='email/welcome_subject.txt')
                messages.success(request, f'{group.name} account has been created.')
                return redirect('signup')
    else:
        user = SignupForm()
        profile = ProfileForm()
    context = {'user':user,'profile':profile,}
    return render(request, 'backoffice/account_pages/signup.html', context)

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
            messages.success(request, ' Your Profile has been updated.')
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
        messages.success(request, "Password has been changed.")
        return redirect('userprofile')
    context={'form':form,}
    return render(request, 'backoffice/account_pages/change_password.html', context)


#################################################################################################################################
#################################################################################################################################
@login_required(login_url='signin')
@admin_only
def ProjectCreateView(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        form2 = ProjectBlueprintForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        if form.is_valid() and form2.is_valid():
            project = form.save()
            form2.save(commit=False)
            for f in files:
                image = ProjectBlueprint(project=project, image=f)
                image.save()
            messages.success(request, 'Project has been created.')
            return redirect('project_list')
        else:
            messages.error(request, 'Failed on Creating Project')
            return redirect('project_create')
    else:
        form = ProjectForm()
        form2 = ProjectBlueprintForm()
    context = {'form':form, 'form2':form2}
    return render(request, 'backoffice/project_pages/project_create.html', context)

@login_required(login_url='signin')
@allowed_users(allowed_roles=['Admin','Project Manager'])
def ProjectUpdateView(request,pk):
    data = Project.objects.get(id=pk)
    if request.method == 'POST':
        form = ProjectUpdateForm(request.POST, instance=data)
        form2 = ProjectBlueprintForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        if form.is_valid() and form2.is_valid():
            project = form.save()
            form2.save(commit=False)
            for f in files:
                image = ProjectBlueprint(project=project, image=f)
                image.save()
            #notification    
            admin = User.objects.filter(groups__name="Admin")
            for i in admin:
                adnin_notif = Notification.objects.create(receiver=i, description=f"Project {project.project} has been updated", url=f"/project/view/{project.id}")
            client_notif = Notification.objects.create(receiver=project.client, description=f"Project {project.project} has been updated", url=f"/myproject/view/{project.id}")
            pm_notif = Notification.objects.create(receiver=project.pm, description=f"Project {project.project} has been updated", url=f"/project/view/{project.id}")
            if project.pic:
                pic_notif = Notification.objects.create(receiver=project.pic, description=f"Project {project.project} has been updated", url=f"/project/view/{project.id}")
            if project.whm:
                whm_notif = Notification.objects.create(receiver=project.whm, description=f"Project {project.project} has been updated", url=f"/project/view/{project.id}")
            messages.success(request, 'Project Details has been updated.')
            return redirect('project_detail', pk=data.id)
    else:
        form = ProjectUpdateForm(instance=data)
        form2 = ProjectBlueprintForm()
    context = {'form':form, 'data':data, 'form2':form2}
    return render(request, 'backoffice/project_pages/project_update.html', context)

@login_required(login_url='signin')
@admin_only
def ProjectListView(request):
    data = Project.objects.all()
    data2 = Project.objects.filter(status="Completed")
    data3 = Project.objects.filter(status="On-going")
    data4 = Project.objects.filter(status="Pending")
    data5 = Project.objects.filter(status="Completed (Overdue)")
    completed = data2.count()
    ongoing = data3.count()
    pending = data4.count()
    overdue = data5.count()
    context={'data':data, 'completed':completed, 'ongoing':ongoing, 'pending':pending, 'overdue':overdue}
    return render(request,'backoffice/project_pages/project_list.html', context)

@login_required(login_url='signin')
@pm_only
def ProjectListView_PM(request):
    data = Project.objects.filter(pm=request.user)
    data2 = Project.objects.filter(pm=request.user, status="Completed")
    data3 = Project.objects.filter(pm=request.user, status="On-going")
    data4 = Project.objects.filter(pm=request.user, status="Pending")
    data5 = Project.objects.filter(pm=request.user, status="Completed (Overdue)")
    completed = data2.count()
    ongoing = data3.count()
    pending = data4.count()
    overdue = data5.count()
    context={'data':data, 'completed':completed, 'ongoing':ongoing, 'pending':pending, 'overdue':overdue}
    return render(request,'backoffice/project_pages/project_list.html', context)

@login_required(login_url='signin')
@pic_only
def ProjectListView_PIC(request):
    data = Project.objects.filter(pic=request.user)
    data2 = Project.objects.filter(pic=request.user, status="Completed")
    data3 = Project.objects.filter(pic=request.user, status="On-going")
    data4 = Project.objects.filter(pic=request.user, status="Pending")
    data5 = Project.objects.filter(pic=request.user, status="Completed (Overdue)")
    completed = data2.count()
    ongoing = data3.count()
    pending = data4.count()
    overdue = data5.count()
    context={'data':data, 'completed':completed, 'ongoing':ongoing, 'pending':pending, 'overdue':overdue}
    return render(request,'backoffice/project_pages/project_list.html', context)

@login_required(login_url='signin')
@whm_only
def ProjectListView_WHM(request):
    data = Project.objects.filter(whm=request.user)
    data2 = Project.objects.filter(whm=request.user, status="Completed")
    data3 = Project.objects.filter(whm=request.user, status="On-going")
    data4 = Project.objects.filter(whm=request.user, status="Pending")
    data5 = Project.objects.filter(whm=request.user, status="Completed (Overdue)")
    completed = data2.count()
    ongoing = data3.count()
    pending = data4.count()
    overdue = data5.count()
    context={'data':data, 'completed':completed, 'ongoing':ongoing, 'pending':pending, 'overdue':overdue}
    return render(request,'backoffice/project_pages/project_list.html', context)

@login_required(login_url='signin')
@staff_only
def ProjectDetailView(request, pk):
    try:
        data = Project.objects.get(id=pk)
        blueprint = ProjectBlueprint.objects.filter(project_id=data.id)
        quotation = Quotation.objects.filter(project_id=data.id)
        inventory = ProjectInventory.objects.filter(project_id=data.id)
        ex_inventory = ExternalProjectInventory.objects.filter(project_id=data.id)
        requisition = Requisition.objects.filter(project_id=data.id)
        external_order = ExternalOrder.objects.filter(project_id=data.id)
        joborder = JobOrder.objects.filter(project_id=data.id)
        rework = Rework.objects.filter(project_id=data.id)
        sitephotos = SitePhotos.objects.filter(project_id=data.id)
        try:
            data2 = ProjectProgress.objects.get(project_id=data.id)
            data3 = ProjectProgressDetails.objects.filter(projectprogress=data2.id)
        except ObjectDoesNotExist:
            context={
                'data':data, 'blueprint':blueprint,
                'quotation':quotation, 'inventory':inventory,
                'requisition':requisition, 'external_order':external_order, 'rework':rework,
                'sitephotos':sitephotos, 'joborder':joborder, 'ex_inventory':ex_inventory,
            }
            return render(request, 'backoffice/project_pages/project_detail.html', context)
        context={
            'data':data, 'data2':data2, 'data3':data3, 'blueprint':blueprint,
            'quotation':quotation, 'inventory':inventory,
            'requisition':requisition, 'external_order':external_order, 'rework':rework,
            'joborder':joborder,  'sitephotos':sitephotos, 'ex_inventory':ex_inventory,
        }
        return render(request, 'backoffice/project_pages/project_detail.html', context)
    except ObjectDoesNotExist:
        return render(request, "404.html")

@login_required(login_url='signin')
@staff_only
def ProjectBlueprintUpdateView(request, pk):
    project = Project.objects.get(id=pk)
    data = ProjectBlueprint.objects.filter(project=project)
    if request.method == "POST":
        formset = ProjectBlueprintFormset(request.POST, request.FILES, instance=project)
        if formset.is_valid():
            data = formset.save()
            messages.success(request, "Blueprint has been updated")
            return redirect('project_detail', pk=project.id)
    else:
        formset = ProjectBlueprintFormset(instance=project)
    context= {'formset':formset, 'data':data, 'project':project}
    return render(request, 'backoffice/project_pages/blueprint_update.html', context)

#################################################################################################################################
#################################################################################################################################
class QuotationCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url ="signin"
    redirect_field_name="redirect_to"
    form_class = QuotationForm
    template_name ='backoffice/quotation_pages/quotation_create.html'
    success_message = "Quotation has been created"
    
    @method_decorator(pm_only, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

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
        quotation = form.save()
        if formset.is_valid():
            formset.instance = quotation
            quotation_list = formset.save()
            #reset quotation total amount
            quotation.total = 0
            #logic ~ set unit cost and get total amount from requistion details
            for i in quotation_list:
                quotation.total += i.amount
                quotation.save()
            return super(QuotationCreateView, self).form_valid(form)
    def form_invalid(self, form):
        print(form.errors)
    def get_success_url(self):
        data = self.object
        data2 = data.project.id
        return reverse_lazy("project_detail", kwargs={'pk': data2})

@login_required(login_url='signin')
@admin_only
def QuotationListView(request):
    data = Quotation.objects.all().order_by('-date')
    data2 = QuotationDetails.objects.all()
    data3 = Quotation.objects.filter(status="Accepted")
    data4 = Quotation.objects.filter(status="Pending")
    data5 = Quotation.objects.filter(status="Rejected")
    accepted = data3.count()
    pending = data4.count()
    rejected = data5.count()
    context={
        'data':data ,'data2':data2, 'accepted':accepted, 
        'pending':pending, 'rejected':rejected,}
    return render(request, 'backoffice/quotation_pages/quotation_list.html', context)

@login_required(login_url='signin')
@pm_only
def QuotationListView_PM(request):
    project = Project.objects.filter(pm=request.user)
    data = Quotation.objects.filter(project__in=project).order_by('-date')
    data3 = Quotation.objects.filter(project__in=project, status="Accepted")
    data4 = Quotation.objects.filter(project__in=project, status="Pending")
    data5 = Quotation.objects.filter(project__in=project, status="Rejected")
    accepted = data3.count()
    pending = data4.count()
    rejected = data5.count()
    context={
        'data':data ,'accepted':accepted, 
        'pending':pending, 'rejected':rejected,}
    return render(request, 'backoffice/quotation_pages/quotation_list.html', context)

@login_required(login_url='signin')
@allowed_users(allowed_roles=['Admin','Project Manager'])
def QuotationDetailView(request,pk):
    try:
        data = Quotation.objects.get(id=pk)
        project = Project.objects.get(id=data.project.id)
        data2 = QuotationDetails.objects.filter(quotation=data.id)
        #creating project progress
        if request.method == "POST":
            #try creating project progress. 
            try:
                #if exist, returns error message.
                data3 = ProjectProgress.objects.get(project=data.project.id)
                messages.warning(request, "There is an existing Work Progress. Please delete the previous one to create a new Work Progress.")
                return redirect('quotation_detail',pk=data.id)
            except ObjectDoesNotExist:
                #if doesn't exist, create project progress
                data3 = ProjectProgress.objects.create(project=data.project)
                for i in data2:
                    data4 = ProjectProgressDetails.objects.create(projectprogress=data3, scope_of_work=i.scope_of_work)
                project.status = "On-going"
                project.save()
                messages.success(request, "Work Progress has been created.")
                return redirect('project_detail',pk=project.id)
        context = { 'data':data, 'data2':data2 }
        return render(request, 'backoffice/quotation_pages/quotation_detail.html', context)
    except ObjectDoesNotExist:
        return render(request, "404.html")

@login_required(login_url='signin')
@allowed_users(allowed_roles=['Admin','Project Manager'])
def QuotationDeleteView(request,pk):
    data = Quotation.objects.get(id=pk)
    data2 = QuotationDetails.objects.filter(quotation=data.id)
    if request.method == 'POST':
        data.delete()
        messages.success(request, 'Quotation has been deleted.')
        return redirect('project_detail', pk=data.project.id)
    context={'data':data,'data2':data2,}
    return render(request, 'backoffice/quotation_pages/quotation_delete.html', context)

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Project Manager'])
def ProgressUpdateView(request,pk):
    data = ProjectProgress.objects.get(id=pk)
    data2 = ProjectProgressDetails.objects.filter(projectprogress=data.id)
    data3 = Project.objects.get(project=data.project)
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
                    i.completion_date = datetime.date.today()
                    i.save()
                    dividend+=i.level
                elif i.status == "On-going":
                    i.start_date = datetime.date.today()
                    i.completion_date = None
                    i.save()
                else:
                    i.start_date = None
                    i.completion_date = None
                    i.save()
            percentage = (dividend/divisor)*100
            data.total_progress = percentage
            data.save()
            messages.success(request,"Progress has been updated.")
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
    data3 = Project.objects.get(project=data.project)
    formset = ProgressFormset()
    if request.method == "POST":
        data.delete()
        data3.status ="Pending"
        data3.save()
        messages.success(request, "Work Progress has been deleted")
        return redirect('project_detail', pk=data3.id)
    else:
        formset = ProgressFormset(instance=data)
    
    context={'formset':formset, 'data':data, 'data2':data2,}
    return render(request, 'backoffice/project_pages/progress_delete.html', context)

#################################################################################################################################
#################################################################################################################################
@admin_only
def InquiryListView(request):
    data = Inquiry.objects.all().order_by('-date_created')
    context = {'data':data}
    return render(request, 'backoffice/project_pages/inquiry_list.html', context)

@admin_only
def InquiryDetailView(request, pk):
    try:
        data = Inquiry.objects.get(id=pk)
        if request.method == "POST":
            status = request.POST.get("status")
            if status == "read":
                data.status = True
                data.save()
                return redirect('inquiry_detail', pk=data.id)
            elif status == "unread":
                data.status = False
                data.save()
                return redirect('inquiry_detail', pk=data.id)
        context = {'data':data}
        return render(request, 'backoffice/project_pages/inquiry_detail.html', context)
    except ObjectDoesNotExist:
        return render(request, "404.html")

@admin_only
def InquiryDeleteView(request, pk):
    data = Inquiry.objects.get(id=pk)
    if request.method == "POST":
        data.delete()
        messages.success(request, "Inquiry has been deleted")
        return redirect('inquiry_list')
    context = {'data':data}
    return render(request, 'backoffice/project_pages/inquiry_delete.html', context)

@admin_only
def EstimateListView(request):
    data = Estimate.objects.all().order_by('-date_created')
    context = {'data':data}
    return render(request, 'backoffice/project_pages/estimate_list.html', context)
    
@admin_only
def EstimateDetailView(request, pk):
    try:
        data = Estimate.objects.get(id=pk)
        data2 = EstimateImage.objects.filter(estimate=data)
        if request.method == "POST":
            status = request.POST.get("status")
            if status == "read":
                data.status = True
                data.save()
                return redirect('estimate_detail', pk=data.id)
            elif status == "unread":
                data.status = False
                data.save()
                return redirect('estimate_detail', pk=data.id)
        context = {'data':data , 'data2':data2}
        return render(request, 'backoffice/project_pages/estimate_detail.html', context)
    except ObjectDoesNotExist:
        return render(request, "404.html")
    
@admin_only
def EstimateDeleteView(request, pk):
    data = Estimate.objects.get(id=pk)
    data2 = EstimateImage.objects.filter(estimate=data)
    if request.method == "POST":
        data.delete()
        messages.success(request, "Estimate Form has been deleted")
        return redirect('estimate_list')
    context = {'data':data}
    return render(request, 'backoffice/project_pages/estimate_delete.html', context)

#################################################################################################################################
#################################################################################################################################
class RequisitionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url ="signin"
    redirect_field_name = "redirect_to"
    form_class = RequisitionForm
    template_name = 'backoffice/requisition_pages/requisition_create.html'
    success_message = "Requisition has been created"
    
    @method_decorator(whm_only, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super(RequisitionCreateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["formset"] = RequisitionFormSet(self.request.POST)
        else:
            data["formset"] = RequisitionFormSet()
        return data
    
    def get_initial(self):
        return { 'whm':self.request.user }

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        requisition = form.save()
        if formset.is_valid():
            formset.instance = requisition
            requisitiondetails = formset.save(False)
            for i in requisitiondetails:
                item = Inventory.objects.get(description=i.articles)
                data2 = RequisitionDelivery.objects.create(requisition=i.requisition,articles=i.articles, unit_price=item.unit_price, unit=item.unit)
            formset.save()
            return super(RequisitionCreateView, self).form_valid(form)
    def get_success_url(self):
        return reverse_lazy("requisition_create")

class RequisitionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url ="signin"
    redirect_field_name = "redirect_to"
    model = Requisition
    fields = ('date',)
    template_name = 'backoffice/requisition_pages/requisition_update.html'
    success_message = "Requisition has been updated"

    @method_decorator(whm_only, name='dispatch')
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
        requisition = form.save()
        if formset.is_valid():
            formset.instance = requisition
            requisitiondetails = formset.save(False)
            qs = RequisitionDelivery.objects.filter(requisition=requisition.id)
            qs.delete()
            for i in requisitiondetails:
                data2 = RequisitionDelivery.objects.create(requisition=i.requisition,articles=i.articles)
            formset.save()
            project = Project.objects.get(id=requisition.project.id)
            admin = User.objects.filter(groups__name="Admin")
            for i in admin:
                adnin_notif = Notification.objects.create(receiver=i, description=f"{requisition.whm} has updated the requisition on  Project {requisition.project}", url=f"/materials/requisition/{requisition.id}")
            pm_notif = Notification.objects.create(receiver=project.pm, description=f"{requisition.whm} has updated the requisition on  Project {requisition.project}", url=f"/materials/requisition/{requisition.id}")
            pic_notif = Notification.objects.create(receiver=project.pic, description=f"{requisition.whm} has updated the requisition on  Project {requisition.project}", url=f"/materials/requisition/{requisition.id}")
            return super().form_valid(form)

    def get_success_url(self):
        data=self.kwargs['pk']
        return reverse_lazy("requisition_detail", kwargs={'pk': data})

@login_required(login_url='signin')
@admin_only
def RequisitionListView(request):
    data = Requisition.objects.all().order_by('-date')
    data2 = RequisitionDetails.objects.all()
    data3 = Requisition.objects.filter(status="Pending")
    data4 = Requisition.objects.filter(status="To be Delivered")
    data5 = Requisition.objects.filter(status="Closed")
    data6 = Requisition.objects.filter(status="Incomplete Order (Closed)")
    pending = data3.count()
    delivered = data4.count()
    closed = data5.count()
    incomplete = data6.count()
    context = {'data':data, 'data2':data2, 'pending':pending, 'delivered':delivered, 'closed':closed, 'incomplete':incomplete}
    return render(request, 'backoffice/requisition_pages/requisition_list.html',context)

@login_required(login_url='signin')
@pm_only
def RequisitionListView_PM(request):
    project = Project.objects.filter(pm=request.user)
    data = Requisition.objects.filter(project__in=project).order_by('-date')
    data2 = RequisitionDetails.objects.all()
    data3 = Requisition.objects.filter(project__in=project, status="Pending")
    data4 = Requisition.objects.filter(project__in=project, status="To be Delivered")
    data5 = Requisition.objects.filter(project__in=project, status="Closed")
    data6 = Requisition.objects.filter(project__in=project, status="Incomplete Order (Closed)")
    pending = data3.count()
    delivered = data4.count()
    closed = data5.count()
    incomplete = data6.count()
    context = {'data':data, 'data2':data2, 'pending':pending, 'delivered':delivered, 'closed':closed, 'incomplete':incomplete}
    return render(request, 'backoffice/requisition_pages/requisition_list.html',context)

@login_required(login_url='signin')
@allowed_users(allowed_roles=['Person In-Charge'])
def RequisitionListView_PIC(request):
    project = Project.objects.filter(pic=request.user)
    data = Requisition.objects.filter(project__in=project).order_by('-date')
    data2 = RequisitionDetails.objects.all()
    data3 = Requisition.objects.filter(project__in=project, status="Pending")
    data4 = Requisition.objects.filter(project__in=project, status="To be Delivered")
    data5 = Requisition.objects.filter(project__in=project, status="Closed")
    data6 = Requisition.objects.filter(project__in=project, status="Incomplete Order (Closed)")
    pending = data3.count()
    delivered = data4.count()
    closed = data5.count()
    incomplete = data6.count()
    context = {'data':data, 'data2':data2, 'pending':pending, 'delivered':delivered, 'closed':closed, 'incomplete':incomplete}
    return render(request, 'backoffice/requisition_pages/requisition_list.html',context)

@login_required(login_url='signin')
@whm_only
def RequisitionListView_WHM(request):
    project = Project.objects.filter(whm=request.user)
    data = Requisition.objects.filter(project__in=project).order_by('-date')
    data2 = RequisitionDetails.objects.all()
    data3 = Requisition.objects.filter(project__in=project, status="Pending")
    data4 = Requisition.objects.filter(project__in=project, status="To be Delivered")
    data5 = Requisition.objects.filter(project__in=project, status="Closed")
    data6 = Requisition.objects.filter(project__in=project, status="Incomplete Order (Closed)")
    pending = data3.count()
    delivered = data4.count()
    closed = data5.count()
    incomplete = data6.count()
    context = {'data':data, 'data2':data2, 'pending':pending, 'delivered':delivered, 'closed':closed, 'incomplete':incomplete}
    return render(request, 'backoffice/requisition_pages/requisition_list.html',context)

@login_required(login_url='signin')
@staff_only
def RequisitionDetailView(request, pk):
    try:
        data = Requisition.objects.get(id=pk)
        data2 = RequisitionDetails.objects.filter(requisition=data.id)
        data3 = RequisitionImage.objects.filter(requisition=data.id)
        data4 = RequisitionDelivery.objects.filter(requisition=data.id).order_by('status', 'articles')
        context= {'data':data, 'data2':data2, 'data3':data3, 'data4':data4,}
        return render(request, 'backoffice/requisition_pages/requisition_detail.html', context)
    except ObjectDoesNotExist:
        return render(request, "404.html")

@login_required(login_url='signin')
@allowed_users(allowed_roles=['Admin','Warehouseman'])
def RequisitionDeleteView(request, pk):
    data = Requisition.objects.get(id=pk)
    data2 = RequisitionDetails.objects.filter(requisition=data.id)
    if request.method == 'POST':
        data.delete()
        messages.success(request, 'Requisition has been deleted.', extra_tags='success')
        group = request.user.groups.all()[0].name
        if group == "Warehouseman":
            return redirect("requisition_list_whm")
        elif group == "Person In-Charge":
            return redirect("requisition_list_pic")
        elif group == "Project Manager":
            return redirect("requisition_list_pic")
        elif group == "Admin":
            return redirect("requisition_list")

    context= {'data':data, 'data2':data2, }
    return render(request, 'backoffice/requisition_pages/requisition_delete.html', context)

@login_required(login_url='signin')
@admin_only
def RequisitionActionView(request,pk):
    data = Requisition.objects.get(id=pk)
    data2 = RequisitionDetails.objects.filter(requisition=data.id)
    data3 = RequisitionDelivery.objects.filter(requisition=data.id)
    if request.method == 'POST':
        formset = RequisitionActionFormSet(request.POST, instance=data)
        if data.status == "Closed" or data.status =="To be Delivered":
            messages.warning(request, "Cannot update Requistion because it's already been complied")
            return redirect('requisition_detail',pk=data.id)
        else:
            if formset.is_valid():
                delivery = formset.save(False)
                for i in delivery:
                    if i.status == "To be delivered":
                        item = Inventory.objects.get(description=i.articles)
                        #check if quantity on requisition is greater than on Inventory 
                        if item.quantity < i.quantity:
                            messages.error(request, f"Quantity of {i.articles} on Inventory Office are not sufficient to comply requisition. Please update your stocks or canceled the item request.")
                            return redirect('requisition_action', pk=data.id)
                        # check if item has price
                        if item.unit_price is None or item.unit_price == 0:
                            messages.error(request, f'"{i.articles}" has no unit price. Please update its unit price on Material Inventory Office')
                            return redirect('requisition_action', pk=data.id)
                    elif i.status =="Canceled":
                        i.quantity = 0
                formset.save()
                canceled = RequisitionDelivery.objects.filter(requisition=data.id, status="Canceled")
                #process logic   
                for i in data3:
                    if i.status == "To be delivered":
                        item =Inventory.objects.get(description=i.articles)
                        item.quantity -= i.quantity
                        item.save()
                        # data.amount += i.quantity*i.articles.unit_price
                        # data.save()
                    elif i.status == "Canceled":
                        i.quantity = 0
                        i.save()
                data.amount = 0
                for j in data3:
                    if j.status != "Canceled":
                        data.amount += j.total_price()
                        data.save()
                if data3.count() == canceled.count():
                    data.status = "Closed"
                    data.save()
                else:
                    data.status = "To be Delivered"
                    data.save()
                whm_notif = Notification.objects.create(receiver=data.whm, description=f"The Admin has complied to your requisition", url=f"/materials/requisition/{data.id}")
                messages.success(request, "Requisition has been complied.")
                return redirect('requisition_detail',pk=data.id)
            else:
                return redirect('requisition_detail',pk=data.id)
    else:
        formset = RequisitionActionFormSet(instance=data)
    context={'formset':formset, 'data':data, 'data2':data2}
    return render(request, 'backoffice/requisition_pages/requisition_action.html', context)
    
@login_required(login_url='signin')
@whm_only    
def RequisitionActionView_WHM(request,pk):
    data = Requisition.objects.get(id=pk)
    data2 = RequisitionDelivery.objects.filter(requisition=data.id)
    queryset = RequisitionDelivery.objects.exclude(Q(status="Canceled"))
    if request.method == 'POST':
        form = RequisitionImageForm(request.POST, request.FILES)
        formset = RequisitionActionFormSet_whm(request.POST, instance=data, queryset=queryset)
        files = request.FILES.getlist('image')
        if data.status != "Completed":
            if form.is_valid() and formset.is_valid():
                formset.save()
                for i in data2:
                    if i.status2 == "Complete":
                        i.quantity2 = i.quantity
                    elif i.status2 == "Incomplete":
                        if i.quantity < i.quantity2:
                            for j in data2:
                                j.status2 = None
                                j.quantity2 = None
                                j.save()
                            messages.error(request,"Received Quantity cannot be higher than Delivered Quantity ")
                            return redirect("requisition_action_whm", pk=data.id)
                        elif i.quantity == i.quantity2:
                            for j in data2:
                                j.status2 = None
                                j.quantity2 = None
                                j.save()
                            messages.error(request,'Received Quantity cannot be equal to the Delivered Quantity when selected in action is "Incomplete"')
                            return redirect("requisition_action_whm", pk=data.id)
                        elif i.quantity2 == 0:
                            for j in data2:
                                j.status2 = None
                                j.quantity2 = None
                                j.save()
                            messages.error(request,'Please check your fields before you submit it"')
                            return redirect("requisition_action_whm", pk=data.id)
                    else:
                        i.quantity2=None
                        i.save()
                try:
                    data3 =  ProjectInventory.objects.get(project=data.project)
                    for k in data2:
                        if k.status2 !="Not Received" and k.status !="Pending" and k.status !="Canceled":
                            try:
                                data4 = ProjectInventoryDetails.objects.get(inventory=data3,articles=k.articles, unit=k.unit)
                                data4.quantity += k.quantity2
                                k.save()
                                data4.save()
                            except ObjectDoesNotExist:
                                data4 = ProjectInventoryDetails.objects.create(inventory=data3, articles=k.articles, quantity=k.quantity2, unit=k.unit)
                                k.save()
                    data3.last_update = datetime.date.today()
                    data3.save()
                    data.status = "Closed"
                    data.save()
                    for l in data2:
                        if l.status2 == "Not Received" or l.status == "Incomplete":
                            data.status = "Incomplete Order (Closed)"
                            data.save()
                    form.save(False)
                    for f in files:
                        image = RequisitionImage(requisition=data, image=f)
                        image.save()
                    messages.success(request, "Delivered Items has been added to Inventory.")
                    return redirect('requisition_detail',pk=data.id)
                except ObjectDoesNotExist:
                    data3 = ProjectInventory.objects.create(project=data.project)
                    for k in data2:
                        if k.status2 !="Not Received" and k.status !="Pending" and k.status !="Canceled":
                            try:
                                data4 = ProjectInventoryDetails.objects.get(inventory=data3, articles=k.articles, unit=k.unit)
                                data4.quantity += k.quantity2
                                k.save()
                                data4.save()
                            except ObjectDoesNotExist:
                                data4 = ProjectInventoryDetails.objects.create(inventory=data3, articles=k.articles, quantity=k.quantity2, unit=k.unit)
                                k.save()
                    data3.last_update = datetime.date.today()
                    data3.save()
                    data.status = "Closed"
                    data.save()
                    for l in data2:
                        if l.status2 == "Not Received" or l.status == "Incomplete":
                            data.status = "Incomplete Order (Closed)"
                            data.save()
                    form.save(False)
                    for f in files:
                        image = RequisitionImage(requisition=data, image=f)
                        image.save()
                    admin = User.objects.filter(groups__name="Admin")
                    for i in admin:
                        adnin_notif = Notification.objects.create(receiver=i, description=f"{data.whm} has updated the delivery requisition on the project {data.project}", url=f"/materials/requisition/{data.id}")
                    messages.success(request, "Delivered Items has been added to Inventory.")
                    return redirect('requisition_detail',pk=data.id)    
            else:
                print(formset.errors)
                return redirect('requisition_detail',pk=data.id)
        else:
            messages.error(request, "This Requisition has been already added to inventory")
            return redirect('requisition_detail', pk=data.id)
    else:
        form = RequisitionImageForm()
        formset = RequisitionActionFormSet_whm(instance=data, queryset=queryset)
    context={'form':form, 'formset':formset, 'data':data, 'data2':data2, }
    return render(request, 'backoffice/requisition_pages/requisition_action_whm.html', context)

@login_required(login_url='signin')
@pic_only
def RequisitionUpdatePIC(request, pk):
    data = Requisition.objects.get(id=pk)
    data2 = RequisitionDetails.objects.filter(requisition=data.id)
    data3 = RequisitionImage.objects.filter(requisition=data.id)
    data4 = RequisitionDelivery.objects.filter(requisition=data.id)
    if request.method == "POST":
        form = RequisitionPICForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            admin = User.objects.filter(groups__name="Admin")
            for i in admin:
                adnin_notif = Notification.objects.create(receiver=i, description=f"{data.project.pic} has updated the requisition number on the project {data.project}", url=f"/materials/requisition/{data.id}")
            messages.success(request, "Requisition Number has been updated")
            return redirect('requisition_detail', pk=data.id)
    else:
        form = RequisitionPICForm(instance=data)
    context = {'form':form, 'data':data, 'data2':data2, 'data3':data3, 'data4':data4,}
    return render(request, 'backoffice/requisition_pages/requisition_pic.html', context)
#################################################################################################################################
#################################################################################################################################
@login_required(login_url='signin')
@admin_only
def ProjectInventoryListView(request):
    data2 = ProjectInventory.objects.all()
    context = {'data2':data2}
    return render(request, 'backoffice/inventory_pages/inventory_list.html', context)

@login_required(login_url='signin')
@admin_only
def ExternalProjectInventoryListView(request):
    data2 = ExternalProjectInventory.objects.all()
    context = {'data2':data2}
    return render(request, 'backoffice/inventory_pages/externalorder_inventory_list.html', context)

@login_required(login_url='signin')
@whm_only
def ProjectInventoryList_WHM(request):
    user = request.user
    data = Project.objects.filter(whm=user)
    data2 = ProjectInventory.objects.filter(project__in=data)
    context = {'data2':data2}
    return render(request, 'backoffice/inventory_pages/inventory_list.html', context)

@login_required(login_url='signin')
@whm_only
def ExternalProjectInventoryList_WHM(request):
    user = request.user
    data = Project.objects.filter(whm=user)
    data2 = ExternalProjectInventory.objects.filter(project__in=data)
    context = {'data2':data2}
    return render(request, 'backoffice/inventory_pages/externalorder_inventory_list.html', context)

@login_required(login_url='signin')
@pm_only
def ProjectInventoryList_PM(request):
    user = request.user
    data = Project.objects.filter(pm=user)
    data2 = ProjectInventory.objects.filter(project__in=data)
    context = {'data2':data2}
    return render(request, 'backoffice/inventory_pages/inventory_list.html', context)

@login_required(login_url='signin')
@pm_only
def ExternalProjectInventoryList_PM(request):
    user = request.user
    data = Project.objects.filter(pm=user)
    data2 = ExternalProjectInventory.objects.filter(project__in=data)
    context = {'data2':data2}
    return render(request, 'backoffice/inventory_pages/externalorder_inventory_list.html', context)

@login_required(login_url='signin')
@pic_only
def ProjectInventoryList_PIC(request):
    user = request.user
    data = Project.objects.filter(pic=user)
    data2 = ProjectInventory.objects.filter(project__in=data)
    context = {'data2':data2}
    return render(request, 'backoffice/inventory_pages/inventory_list.html', context)

@login_required(login_url='signin')
@pic_only
def ExternalProjectInventoryList_PIC(request):
    user = request.user
    data = Project.objects.filter(pic=user)
    data2 = ExternalProjectInventory.objects.filter(project__in=data)
    context = {'data2':data2}
    return render(request, 'backoffice/inventory_pages/externalorder_inventory_list.html', context)

@login_required(login_url='signin')
@staff_only
def ProjectInventoryDetailView(request,pk):
    try:
        data = ProjectInventory.objects.get(id=pk)
        data2 = ProjectInventoryDetails.objects.filter(inventory=data).order_by('articles')
        context = {'data':data, 'data2':data2}
        return render(request, 'backoffice/inventory_pages/inventory_detail.html', context)
    except ObjectDoesNotExist:
        return render(request, "404.html")

@login_required(login_url='signin')
@staff_only
def ExternalProjectInventoryDetailView(request,pk):
    try:
        data = ExternalProjectInventory.objects.get(id=pk)
        data2 = ExternalProjectInventoryDetails.objects.filter(inventory=data).order_by('articles')
        context = {'data':data, 'data2':data2}
        return render(request, 'backoffice/inventory_pages/externalorder_inventory_detail.html', context)
    except ObjectDoesNotExist:
        return render(request, "404.html")

@login_required(login_url='signin')
@whm_only
def ProjectInventoryReport_WHM(request,pk):
    data = ProjectInventory.objects.get(id=pk)
    data2 = ProjectInventoryDetails.objects.filter(inventory=data).order_by('articles')
    if request.method == 'POST':
        form = DailyReportForm(request.POST)
        formset = DailyReportFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            form = form.save(False)
            formset = formset.save(False)
            # check if articles in forms exist on inventory
            for i in formset:
                try:
                    article = ProjectInventoryDetails.objects.get(inventory=data, articles=i.articles)
                except ObjectDoesNotExist:
                    messages.error(request, "Articles on Form does not exist on Inventory")
                    return redirect('inventory_whm_detail', pk=data.id)
            for i in formset:
                item = ProjectInventoryDetails.objects.get(inventory=data, articles=i.articles)
                if item.quantity < i.quantity:
                    messages.error(request, f"Quantity of {i.articles} on Project Site Inventory are not sufficient.")
                    return redirect('inventory_whm_detail', pk=data.id)
            for i in formset:
                for j in data2:
                    if i.articles.articles == j.articles:
                        j.quantity -= i.quantity
                        j.save()
            form.save()
            for i in formset:
                i.report = form
                i.save()
            data.date = datetime.date.today
            data.save()
            project = Project.objects.get(id=data.project.id)
            admin = User.objects.filter(groups__name="Admin")
            for i in admin:
                adnin_notif = Notification.objects.create(receiver=i, description=f"Material Report at project {project.project} has been created ", url=f"/reports/materialreport/{form.id}")
            project = Project.objects.get(id=data.project.id)
            pm_notif = Notification.objects.create(receiver=project.pm, description=f"Material Report at project {project.project} has been created ", url=f"/reports/materialreport/{form.id}")
            pic_notif = Notification.objects.create(receiver=project.pic, description=f"Material Report at project {project.project} has been created ", url=f"/reports/materialreport/{form.id}")
            messages.success(request, "Daily Material Report has been created.")
            return redirect('inventory_whm_detail', pk=data.id)  
        else:
            print(form.errors, formset.errors)
    else:
        form = DailyReportForm(initial={'project':data.project, 'whm':request.user})
        formset = DailyReportFormSet()
        for f in formset:
            f.fields['articles'].queryset = ProjectInventoryDetails.objects.filter(inventory=data)
    context = {'data':data, 'data2':data2, 'form':form, 'formset':formset}
    return render(request, 'backoffice/inventory_pages/inventory_detail_whm.html', context)

@login_required(login_url='signin')
@whm_only
def ExternalProjectInventoryReport_WHM(request,pk):
    data = ExternalProjectInventory.objects.get(id=pk)
    data2 = ExternalProjectInventoryDetails.objects.filter(inventory=data).order_by('articles')
    if request.method == 'POST':
        form = ExternalMaterialReportForm(request.POST)
        formset = ExternalMaterialReportFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            form = form.save(False)
            formset = formset.save(False)
            for i in formset:
                try:
                    article = ExternalProjectInventoryDetails.objects.get(inventory=data, articles=i.articles)
                except ObjectDoesNotExist:
                    messages.error(request, "Invalid Input. Articles on Form does not exist on External Order Inventory")
                    return redirect('external_inventory_whm_detail', pk=data.id)
            for i in formset:
                item = ExternalProjectInventoryDetails.objects.get(inventory=data, articles=i.articles)
                if item.quantity < i.quantity:
                    messages.error(request, f"Quantity of {i.articles} on Project Site External Order Inventory are not sufficient.")
                    return redirect('external_inventory_whm_detail', pk=data.id)
            for i in formset:
                for j in data2:
                    if i.articles.articles == j.articles:
                        j.quantity -= i.quantity
                        j.save()
            form.save()
            for i in formset:
                i.report = form
                i.save()
            data.date=datetime.date.today
            data.save()
            project = Project.objects.get(id=data.project.id)
            admin = User.objects.filter(groups__name="Admin")
            for i in admin:
                adnin_notif = Notification.objects.create(receiver=i, description=f"Material Report has been created at project {project.project}", url=f"/reports/materialreport/external/{data.id}")
            messages.success(request, "Daily Material Report has been created.")
            return redirect('external_inventory_whm_detail', pk=data.id)
    else:
        form = ExternalMaterialReportForm(initial={'project':data.project, 'whm':request.user})
        formset =ExternalMaterialReportFormSet()
        for f in formset:
            f.fields["articles"].queryset = ExternalProjectInventoryDetails.objects.filter(inventory=data)
    context = {'data':data, 'data2':data2, 'form':form, 'formset':formset}
    return render(request, 'backoffice/inventory_pages/externalorder_inventory_detail_whm.html', context)

#################################################################################################################################
#################################################################################################################################
class ExternalOrderCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url ="signin"
    redirect_field_name = "redirect_to"
    form_class = ExternalOrderForm
    template_name ='backoffice/externalorder_pages/externalorder_create.html'
    success_message = "External Order has been created."

    @method_decorator(staff_only, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super(ExternalOrderCreateView, self).dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        return { 'whm':self.request.user }

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["form"] = self.form_class(self.request.POST, self.request.FILES)
            data['files'] = self.request.FILES.getlist('image')
            data["formset"] = ExternalOrderFormSet(self.request.POST)
        else:
            data["formset"] = ExternalOrderFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        files = context['files']
        externalorder = form.save()
        if formset.is_valid():
            formset.instance = externalorder
            externalorderdetail = formset.save()
            externalorder.amount = 0
            for i in externalorderdetail:
                externalorder.amount += i.get_total()
            externalorder.save()
            for f in files:
                image = ExternalOrderImage.objects.create(externalorder=externalorder, image=f)
            try:
                data2 = ExternalProjectInventory.objects.get(project=externalorder.project)
                for i in externalorderdetail:
                    try:
                        data3 = ExternalProjectInventoryDetails.objects.get(articles=i.articles)
                        data3.quantity += i.quantity
                        data3.save()
                    except ObjectDoesNotExist:
                        data3 = ExternalProjectInventoryDetails.objects.create(inventory=data2, articles=i.articles, unit=i.unit, quantity=i.quantity)
            except ObjectDoesNotExist:
                data2 = ExternalProjectInventory.objects.create(project=externalorder.project)
                for i in externalorderdetail:
                    try:
                        data3 = ExternalProjectInventoryDetails.objects.get(articles=i.articles)
                        data3.quantity += i.quantity
                        data3.save()
                    except ObjectDoesNotExist:
                        data3 = ExternalProjectInventoryDetails.objects.create(inventory=data2, articles=i.articles, unit=i.unit, quantity=i.quantity)
            return super(ExternalOrderCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("externalorder_create")

@login_required(login_url = 'signin')
@admin_only
def ExternalOrderListView(request):
    data = ExternalOrder.objects.all().order_by('-date')
    data2 = ExternalOrderDetails.objects.all()
    context = {'data':data,'data2':data2,}
    return render(request, 'backoffice/externalorder_pages/externalorder_list.html', context)

@login_required(login_url = 'signin')
@pm_only
def ExternalOrderListView_PM(request):
    project = Project.objects.filter(pm=request.user)
    data = ExternalOrder.objects.filter(project__in=project).order_by('-date')
    context = {'data':data}
    return render(request, 'backoffice/externalorder_pages/externalorder_list.html', context)

@login_required(login_url = 'signin')
@pic_only
def ExternalOrderListView_PIC(request):
    project = Project.objects.filter(pic=request.user)
    data = ExternalOrder.objects.filter(project__in=project).order_by('-date')
    context = {'data':data}
    return render(request, 'backoffice/externalorder_pages/externalorder_list.html', context)

@login_required(login_url = 'signin')
@whm_only
def ExternalOrderListView_WHM(request):
    project = Project.objects.filter(whm=request.user)
    data = ExternalOrder.objects.filter(project__in=project).order_by('-date')
    context = {'data':data}
    return render(request, 'backoffice/externalorder_pages/externalorder_list.html', context)

@login_required(login_url = 'signin')
@staff_only
def ExternalOrderDetailView(request,pk):
    try:
        data = ExternalOrder.objects.get(id=pk)
        data2 = ExternalOrderDetails.objects.filter(externalorder=data.id)
        data3 = ExternalOrderImage.objects.filter(externalorder=data.id)
        context = {'data':data,'data2':data2, 'data3':data3,}
        return render(request, 'backoffice/externalorder_pages/externalorder_detail.html', context)
    except ObjectDoesNotExist:
        return render(request, "404.html")

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Warehouseman'])
def ExternalOrderDeleteView(request,pk):
    data = ExternalOrder.objects.get(id=pk)
    data2 = ExternalOrderDetails.objects.filter(externalorder=data.id)
    if request.method == 'POST':
        data.delete()
        messages.success(request, 'External Order has been deleted.')
        group = request.user.groups.all()[0].name
        if group == "Warehouseman":
            return redirect("externalorder_list_whm")
        elif group == "Admin":
            return redirect("externalorder_list")
    context = {'data':data,'data2':data2,}
    return render(request, 'backoffice/externalorder_pages/externalorder_delete.html', context)

#################################################################################################################################
#################################################################################################################################
class JobOrderCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url ="signin"
    redirect_field_name = "redirect_to"
    form_class = JobOrderForm
    template_name ='backoffice/joborder_pages/joborder_create.html'
    success_message = "Job Order has been created"
    
    @method_decorator(staff_only, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super(JobOrderCreateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        return { 'pic':self.request.user }

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["formset"] = JobOrderFormSet(self.request.POST)
        else:
            data["formset"] = JobOrderFormSet()
        return data

    def data2(self):
        return Personnel.objects.all()

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        joborder = form.save()
        if formset.is_valid():
            formset.instance = joborder
            joborder_task = formset.save()
            for i in joborder_task:
                personnel_joborder = PersonnelJobOrder.objects.create(personnel=i.personnel, joborder=i)
            personnel = Personnel.objects.all()
            for i in personnel:
                count = JobOrderTask.objects.filter(personnel=i).count()
                i.joborder_count = count
                i.save()
            return super(JobOrderCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("joborder_create")

class JobOrderUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url ="signin"
    redirect_field_name = "redirect_to"
    model = JobOrder
    fields = '__all__'
    template_name ='backoffice/joborder_pages/joborder_update.html'
    success_message = "Job Order has been updated."
    
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
        joborder = form.save()
        if formset.is_valid():
            formset.instance = joborder
            joborder_task = formset.save()
            for i in joborder_task:
                personnel_joborder = PersonnelJobOrder.objects.create(personnel=i.personnel, joborder=i)
            personnel = Personnel.objects.all()
            for i in personnel:
                count = JobOrderTask.objects.filter(Q(personnel=i, status="Pending") | Q(personnel=i,status="On-going")).count()
                i.joborder_count = count
                i.save()
            return super(JobOrderUpdateView, self).form_valid(form)

    def get_success_url(self):
        data=self.kwargs['pk']
        return reverse_lazy("joborder_detail", kwargs={'pk': data})

@login_required(login_url = 'signin')
@admin_only
def JobOrderListView(request):
    data = JobOrder.objects.all().order_by('-date')
    context = {'data':data,}
    return render(request, 'backoffice/joborder_pages/joborder_list.html', context)

@login_required(login_url = 'signin')
@pm_only
def JobOrderListView_PM(request):
    project = Project.objects.filter(pm=request.user)
    data = JobOrder.objects.filter(project__in=project).order_by('-date')
    context = {'data':data,}
    return render(request, 'backoffice/joborder_pages/joborder_list.html', context)

@login_required(login_url = 'signin')
@pic_only
def JobOrderListView_PIC(request):
    project = Project.objects.filter(pic=request.user)
    data = JobOrder.objects.filter(project__in=project).order_by('-date')
    context = {'data':data,}
    return render(request, 'backoffice/joborder_pages/joborder_list.html', context)

@login_required(login_url = 'signin')
@whm_only
def JobOrderListView_WHM(request):
    project = Project.objects.filter(whm=request.user)
    data = JobOrder.objects.filter(project__in=project).order_by('-date')
    context = {'data':data,}
    return render(request, 'backoffice/joborder_pages/joborder_list.html', context)

@login_required(login_url = 'signin')
@whm_only
def JobOrderReportView(request,pk):
    data = JobOrder.objects.get(id=pk)
    data2 = JobOrderTask.objects.exclude(Q(status__contains="Done"))
    if request.method == 'POST':
        formset = JobOrderReportFormSet(request.POST, instance=data)
        if formset.is_valid():
            task = formset.save(False)
            for i in task:
                if i.status == "Done":
                    i.completion_date = datetime.date.today()
                    i.save()
                    if i.date2 < i.completion_date:
                        i.status = "Done (Overdue)"
                        i.save()
                else:
                    data3 = Personnel.objects.get(id=i.personnel.id)
                    data3.project=data.project
                    data3.status = "Currently Assigned"
                    data3.date = i.date
                    data3.date2 = i.date2
                    data3.save()
                    i.completion_date = None
                    i.save()
            formset.save()
            personnel = Personnel.objects.all()
            for i in personnel:
                count = JobOrderTask.objects.filter(Q(personnel=i, status="Pending") | Q(personnel=i,status="On-going")).count()
                i.joborder_count = count
                i.save()
            project = Project.objects.get(id=data.project.id)
            admin = User.objects.filter(groups__name="Admin")
            for i in admin:
                adnin_notif = Notification.objects.create(receiver=i, description=f"Job Order status at project {project.project} has been updated", url=f"/task/joborder/{data.id}")
            pm_notif = Notification.objects.create(receiver=project.pm, description=f"Job Order status at project {project.project} has been updated", url=f"/task/joborder/{data.id}")   
            pic_notif = Notification.objects.create(receiver=project.pic, description=f"Job Order status at project {project.project} has been updated", url=f"/task/joborder/{data.id}")   
            messages.success(request, "Job Order status has been updated.")
            return redirect('joborder_detail', pk=data.id)
        else:
            messages.warning(request, "Failed")
            return redirect('joborder_detail', pk=data.id)
    else:
        formset = JobOrderReportFormSet(instance=data, queryset=data2)
    context = {'formset': formset, 'data':data}
    return render(request, 'backoffice/joborder_pages/joborder_report.html', context)

@login_required(login_url = 'signin')
@staff_only
def JobOrderDetailView(request,pk):
    try:
        data = JobOrder.objects.get(id=pk)
        data2 = JobOrderTask.objects.filter(joborder=data.id)
        context = {'data':data,'data2':data2}
        return render(request, 'backoffice/joborder_pages/joborder_detail.html', context)
    except ObjectDoesNotExist:
        return render(request, "404.html")

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Project Manager','Person In-Charge'])
def JobOrderDeleteView(request,pk):
    data = JobOrder.objects.get(id=pk)
    data2 = JobOrderTask.objects.filter(joborder=data.id)
    if request.method == 'POST':
        data.delete()
        for i in personnel:
            count = JobOrderTask.objects.filter(Q(personnel=i, status="Pending") | Q(personnel=i,status="On-going")).count()
            i.joborder_count = count
            i.save()
        messages.success(request, 'Job Order has been deleted.')
        return redirect("joborder_create")
    context = {'data':data,'data2':data2}
    return render(request, 'backoffice/joborder_pages/joborder_delete.html', context)

#################################################################################################################################
#################################################################################################################################
@login_required(login_url = 'signin')
@admin_only
def PersonnelCreateView(request):
    data = Personnel.objects.all()
    if request.method == 'POST':
        form = PersonnelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New personnel has been added to the list", extra_tags='success')
            return redirect('personnel_create')
        else:
            print(form.errors)
    else:
        form = PersonnelForm()
    context={'form':form, 'data':data}
    return render(request, 'backoffice/personnel_pages/personnel_create.html', context)        

@login_required(login_url = 'signin')
@staff_only
def PersonnelListView(request):
    data = Personnel.objects.all()
    context = {'data':data}
    return render(request, 'backoffice/personnel_pages/personnel_create.html', context)


@login_required(login_url = 'signin')
@staff_only
def PersonnelDetailView(request, pk):
    try:
        data = Personnel.objects.get(id=pk)
        data2 = PersonnelJobOrder.objects.filter(personnel=data)
        context = {'data':data, 'data2':data2}
        return render(request, 'backoffice/personnel_pages/personnel_detail.html', context)
    except ObjectDoesNotExist:
        return render(request, "404.html")

@login_required(login_url = 'signin')
@admin_only
def PersonnelDeleteView(request, pk):
    data = Personnel.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        messages.success(request, 'Personnel has been deleted.')
        return redirect("personnel_create")
    context = {'data':data}
    return render(request, 'backoffice/personnel_pages/personnel_delete.html', context)

@login_required(login_url = 'signin')
@admin_only
def PersonnelUpdateView(request, pk):
    data = Personnel.objects.get(id=pk)
    if request.method == 'POST':
        form = PersonnelForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, "Personnel Information has been updated.")
            return redirect('personnel_detail', pk=data.id)
    else:
        form = PersonnelForm(instance=data)
    context={'form':form, 'data':data}
    return render(request, 'backoffice/personnel_pages/personnel_update.html', context)

#################################################################################################################################
#################################################################################################################################

class ReworkCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url ="signin"
    redirect_field_name = "redirect_to"
    form_class = ReworkNewForm
    template_name ='backoffice/rework_pages/rework_create.html'
    success_message = "Rework Form has been created."
    
    @method_decorator(pm_only, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def reworkqs(self):
        project = Project.objects.filter(pm=self.request.user)
        return Rework.objects.filter(project__in=project).order_by('-date')

    def get_initial(self):
        return { 'pm':self.request.user }

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["form"] = self.form_class(self.request.POST, self.request.FILES)
            data['files'] = self.request.FILES.getlist('image')
        return data
        
    def form_valid(self, form):
        context = self.get_context_data()
        files = context['files']
        rework = form.save()
        for f in files:
            image = ReworkBeforeImage.objects.create(rework=rework, image=f)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("rework_create")

class ReworkUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url ="signin"
    redirect_field_name = "redirect_to"
    model = Rework
    fields =('instruction',)
    template_name ='backoffice/rework_pages/rework_update.html'
    success_message = "Rework Form has been updated."
    
    @method_decorator(staff_only, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        rework = form.save()
        admin = User.objects.filter(groups__name="Admin")
        for i in admin:
            adnin_notif = Notification.objects.create(receiver=i, description=f"Rework at project {rework.project} has been updated", url=f"/task/rework/{rework.id}")
        pic_notif = Notification.objects.create(receiver=rework.project.pic, description=f"Rework at project {rework.project} has been updated", url=f"/task/rework/{rework.id}")
        return super().form_valid(form)

    def get_success_url(self):
        data=self.kwargs['pk']
        return reverse_lazy("rework_detail", kwargs={'pk':data})

@login_required(login_url = 'signin')
@admin_only
def ReworkListView(request):
    data = Rework.objects.all().order_by('-date')
    context={'data':data}
    return render(request, 'backoffice/rework_pages/rework_list.html', context) 

@login_required(login_url = 'signin')
@pm_only
def ReworkListView_PM(request):
    project = Project.objects.filter(pm=request.user)
    data = Rework.objects.filter(project__in=project).order_by('-date')
    context={'data':data}
    return render(request, 'backoffice/rework_pages/rework_list.html', context) 

@login_required(login_url = 'signin')
@pic_only
def ReworkListView_PIC(request):
    project = Project.objects.filter(pic=request.user)
    data = Rework.objects.filter(project__in=project).order_by('-date')
    context={'data':data}
    return render(request, 'backoffice/rework_pages/rework_list.html', context) 

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Project Manager', 'Person In-Charge'])
def ReworkDetailView(request,pk):
    try:
        data = Rework.objects.get(id=pk)
        data2 = ReworkBeforeImage.objects.filter(rework=data.id)
        data3 = ReworkAfterImage.objects.filter(rework=data.id)
        if request.method == "POST":
            form = ReworkBeforeImageForm(request.POST, request.FILES)
            files = request.FILES.getlist('image')
            if form.is_valid():
                form.save(False)
                for f in files:
                    image = ReworkAfterImage.objects.create(rework=data, image=f)
                admin = User.objects.filter(groups__name="Admin")
                for i in admin:
                    adnin_notif = Notification.objects.create(receiver=i, description=f"Rework at project {data.project} has been updated", url=f"/task/rework/{data.id}")
                pm_notif = Notification.objects.create(receiver=data.project.pm, description=f"Rework at project {data.project} has been updated", url=f"/task/rework/{data.id}")
                messages.success(request, "Rework After Image has been updated")
                return redirect('rework_detail', pk=data.id)
        else:
            form = ReworkAfterImageForm()
        context={'data':data, 'data2':data2, 'data3':data3, 'form':form}
        return render(request, 'backoffice/rework_pages/rework_detail.html', context)
    except ObjectDoesNotExist:
        return render(request, "404.html")

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Project Manager', 'Person In-Charge'])
def ReworkDeleteView(request, pk):
    data = Rework.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        messages.success(request, 'Rework has been deleted!.')
        return redirect('rework_create')
    context={'data':data}
    return render(request, 'backoffice/rework_pages/rework_delete.html', context) 

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Project Manager'])
def ReworkBeforeUpdateView(request, pk):
    data = Rework.objects.get(id=pk)
    if request.method == "POST":
        formset = ReworkBeforeFormset(request.POST, request.FILES, instance=data)
        if formset.is_valid():
            formset.save()
            admin = User.objects.filter(groups__name="Admin")
            for i in admin:
                adnin_notif = Notification.objects.create(receiver=i, description=f"Rework at project {data.project} has been updated", url=f"/task/rework/{data.id}")
            pic_notif = Notification.objects.create(receiver=data.project.pic, description=f"Rework at project {data.project} has been updated", url=f"/task/rework/{data.id}")
            messages.success(request, "Rework Before Image has been updated")
            return redirect('rework_detail',pk=data.id)
    else:
        formset = ReworkBeforeFormset(instance=data)
    context = {'formset':formset, 'data':data}
    return render(request, 'backoffice/rework_pages/rework_before.html', context)

@login_required(login_url = 'signin')
@pm_only
def ReworkAfterUpdateView(request, pk):
    data = Rework.objects.get(id=pk)
    if request.method == "POST":
        formset = ReworkAfterFormset(request.POST, request.FILES, instance=data)
        if formset.is_valid():
            formset.save()
            admin = User.objects.filter(groups__name="Admin")
            for i in admin:
                adnin_notif = Notification.objects.create(receiver=i, description=f"Rework at project {data.project} has been updated", url=f"/task/rework/{data.id}")
            pm_notif = Notification.objects.create(receiver=data.project.pm, description=f"Rework at project {data.project} has been updated", url=f"/task/rework/{data.id}")
            messages.success(request, "Rework Before Image has been updated")
            return redirect('rework_detail',pk=data.id)
    else:
        formset = ReworkAfterFormset(instance=data)
    context = {'formset':formset, 'data':data}
    return render(request, 'backoffice/rework_pages/rework_after.html', context)

#################################################################################################################################
#################################################################################################################################

class ProjectIssuesCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url ="signin"
    redirect_field_name = "redirect_to"
    form_class = ProjectIssuesForm
    template_name ='backoffice/report_pages/project_issue/projectissues.html'
    success_message = "Project Issues has been submitted!"
    
    @method_decorator(whm_only, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    
    def data2(self):
        user =self.request.user
        project = Project.objects.filter(whm=user)
        return ProjectIssues.objects.filter(project__in=project)

    def get_initial(self):
        return { 'whm':self.request.user }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("issues")

class ProjectIssuesUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url ="signin"
    redirect_field_name = "redirect_to"
    model = ProjectIssues
    fields =('description',)
    template_name ='backoffice/report_pages/project_issue/projectissues_update.html'
    success_message = "Project Issues has been updated."
    
    @method_decorator(whm_only, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("issues")
    
@login_required(login_url='signin')
@allowed_users(allowed_roles = ['Admin','Warehouseman'])
def ProjectIssuesDeleteView(request,pk):
    data = ProjectIssues.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        messages.success(request, 'Project Issues has been deleted.')
        group = request.user.groups.all()[0].name
        if group == "Warehouseman":
            return redirect('issues')
        elif group == "Admin":
            return redirect('issues_list')
    context ={'data':data}
    return render(request, 'backoffice/report_pages/project_issue/projectissues_delete.html', context)
    
@login_required(login_url='signin')
@admin_only
def ProjectIssuesList(request):
    data = ProjectIssues.objects.all()
    context = {'data':data}
    return render(request, 'backoffice/report_pages/project_issue/projectissues_list.html', context)

@login_required(login_url='signin')
@pm_only
def ProjectIssuesList_PM(request):
    user =request.user
    project = Project.objects.filter(pm=user)
    data = ProjectIssues.objects.filter(project__in=project)
    context = {'data':data}
    return render(request, 'backoffice/report_pages/project_issue/projectissues_list.html', context)

@login_required(login_url='signin')
@pic_only
def ProjectIssuesList_PIC(request):
    user =request.user
    project = Project.objects.filter(pic=user)
    data = ProjectIssues.objects.filter(project__in=project)
    context = {'data':data}
    return render(request, 'backoffice/report_pages/project_issue/projectissues_list.html', context)

@login_required(login_url='signin')
@whm_only
def ProjectIssuesList_WHM(request):
    user =request.user
    project = Project.objects.filter(whm=user)
    data = ProjectIssues.objects.filter(project__in=project)
    context = {'data':data}
    return render(request, 'backoffice/report_pages/project_issue/projectissues_list.html', context)

@login_required(login_url='signin')
@staff_only
def ProjectIssuesDetailView(request,pk):
    try:
        data = ProjectIssues.objects.get(id=pk)
        context = {'data':data}
        return render(request, 'backoffice/report_pages/project_issue/projectissues_detail.html', context)
    except ObjectDoesNotExist:
        return render(request, "404.html")

#################################################################################################################################
#################################################################################################################################
class SitePhotosCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url ="signin"
    redirect_field_name = "redirect_to"
    form_class = SitePhotostForm
    template_name ='backoffice/report_pages/site_photos/sitephotos_create.html'
    success_message = "Daily Site Photos has been submitted!"
    
    @method_decorator(whm_only, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def qs(self):
        project = Project.objects.filter(whm=self.request.user)
        return SitePhotos.objects.filter(project__in=project).order_by('-date')

    def get_initial(self):
        return { 'whm':self.request.user }

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["form2"] = SitePhotostDetailsForm(self.request.POST, self.request.FILES)
            data['files'] = self.request.FILES.getlist('image')
        else:
            data["form2"] = SitePhotostDetailsForm()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        form2 = context["form2"]       
        files = context['files']
        self.object = form.save()
        if form2.is_valid():
            form2 = form2.save(commit=False)
            for f in files:
                image = SitePhotosDetails(sitephotos=self.object, image=f)
                image.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("sitephotos")

@login_required(login_url = 'signin')
@admin_only
def dailysitephotosListView(request):
    data = SitePhotos.objects.all().order_by('-date')
    context={'data':data}
    return render(request, 'backoffice/report_pages/site_photos/sitephotos_list.html', context)

@login_required(login_url = 'signin')
@pm_only
def dailysitephotosListView_PM(request):
    project = Project.objects.filter(pm=request.user)
    data = SitePhotos.objects.filter(project__in=project).order_by('-date')
    context={'data':data}
    return render(request, 'backoffice/report_pages/site_photos/sitephotos_list.html', context)

@login_required(login_url = 'signin')
@pic_only
def dailysitephotosListView_PIC(request):
    project = Project.objects.filter(pic=request.user)
    data = SitePhotos.objects.filter(project__in=project).order_by('-date')
    context={'data':data}
    return render(request, 'backoffice/report_pages/site_photos/sitephotos_list.html', context)

@login_required(login_url = 'signin')
@whm_only
def dailysitephotosListView_WHM(request):
    project = Project.objects.filter(whm=request.user)
    data = SitePhotos.objects.filter(project__in=project).order_by('-date')
    context={'data':data}
    return render(request, 'backoffice/report_pages/site_photos/sitephotos_list.html', context)

@login_required(login_url = 'signin')
@staff_only
def dailysitephotosDetailView(request,pk):
    try:
        data = SitePhotos.objects.get(id=pk)
        data2 = SitePhotosDetails.objects.filter(sitephotos=data)
        context={'data':data, 'data2':data2}
        return render(request, 'backoffice/report_pages/site_photos/sitephotos_detail.html', context)
    except ObjectDoesNotExist:
        return render(request, "404.html")

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Admin','Project Manager', 'Person In-Charge'])
def dailysitephotosUpdateView(request,pk):
    data = SitePhotos.objects.get(id=pk)
    formset = SitePhotostFormset(instance=data)
    if request.method == 'POST':
        formset = SitePhotostFormset(request.POST, instance=data)
        if formset.is_valid():
            data2 = formset.save()
            messages.success(request, "Daily Site Photos has been updated.")
            project = Project.objects.get(id=data.project.id)
            count = 0
            for i in data2:
                if i.reveal == True:
                    count+=1
            if count !=0:
                client_notif = Notification.objects.create(receiver=project.client, description=f"Site Photos at your project {project.project} has been updated", url=f"/myproject/sitephotos/view/{data.id}")
            return redirect('sitephotos_detail', pk=data.id)
    context={'formset':formset, 'data':data}
    return render(request, 'backoffice/report_pages/site_photos/sitephotos_update.html', context)

@login_required(login_url = 'signin')
@staff_only
def dailysitephotosDeleteView(request,pk):
    data = SitePhotos.objects.get(id=pk)
    data2 = SitePhotosDetails.objects.filter(sitephotos=data)
    if request.method == 'POST':
        data2.delete()
        data.delete()
        messages.success(request, "Daily Site Photos has been deleted.")
        group = request.user.groups.all()[0].name
        if group == "Warehouseman":
            return redirect('sitephotos')
        elif group == "Project Manager":
            return redirect('sitephotos_list_pm')
        elif group == "Person In-Charge":
            return redirect('sitephotos_list_pic')
        else:
            return redirect('sitephotos_list')
    context={'data':data, 'data2':data2}
    return render(request, 'backoffice/report_pages/site_photos/sitephotos_delete.html', context)

#################################################################################################################################
#################################################################################################################################
@login_required(login_url = 'signin')
@admin_only
def MaterialReportListView(request):
    data = MaterialReport.objects.all().order_by('-date')
    context = {'data':data,}
    return render(request, 'backoffice/report_pages/material/materialreport_list.html', context)

@login_required(login_url = 'signin')
@pm_only
def MaterialReportListView_PM(request):
    project = Project.objects.filter(pm=request.user)
    data = MaterialReport.objects.filter(project__in=project).order_by('-date')
    context = {'data':data}
    return render(request, 'backoffice/report_pages/material/materialreport_list.html', context)

@login_required(login_url = 'signin')
@pic_only
def MaterialReportListView_PIC(request):
    project = Project.objects.filter(pic=request.user)
    data = MaterialReport.objects.filter(project__in=project).order_by('-date')
    context = {'data':data}
    return render(request, 'backoffice/report_pages/material/materialreport_list.html', context)

@login_required(login_url = 'signin')
@whm_only
def MaterialReportListView_WHM(request):
    project = Project.objects.filter(whm=request.user)
    data = MaterialReport.objects.filter(project__in=project).order_by('-date')
    context = {'data':data}
    return render(request, 'backoffice/report_pages/material/materialreport_list.html', context)

@login_required(login_url = 'signin')
@staff_only
def MaterialReportDetailView(request, pk):
    try:
        data = MaterialReport.objects.get(id=pk)
        data2 = MaterialReportDetails.objects.filter(report=data.id)
        context={'data':data, 'data2':data2}
        return render(request, 'backoffice/report_pages/material/materialreport_detail.html', context)
    except ObjectDoesNotExist:
        return render(request, "404.html")

@login_required(login_url = 'signin')
@admin_only
def MaterialReportDeleteView(request, pk):
    data = MaterialReport.objects.get(id=pk)
    data2 = MaterialReportDetails.objects.filter(report=data.id)
    if request.method == "POST":
        data.delete()
        messages.success(request, "Material Report has been deleted.")
        group = request.user.groups.all()[0].name
        if group == "Warehouseman":
            return redirect("materialreport_list_whm")
        elif group == "Person In-Charge":
            return redirect("materialreport_list_pic")
        elif group == "Project Manager":
            return redirect("materialreport_list_pic")
        elif group == "Admin":
            return redirect("materialreport_list")
    context={'data':data, 'data2':data2}
    return render(request, 'backoffice/report_pages/material/materialreport_delete.html', context)

@login_required(login_url = 'signin')
@admin_only
def ExternalMaterialReportListView(request):
    data = ExternalMaterialReport.objects.all().order_by('-date')
    context = {'data':data}
    return render(request, 'backoffice/report_pages/external_material/external_report_list.html', context)


@login_required(login_url = 'signin')
@pm_only
def ExternalMaterialReportListView_PM(request):
    project = Project.objects.filter(pm=request.user)
    data = ExternalMaterialReport.objects.filter(project__in=project).order_by('-date')
    context = {'data':data}
    return render(request, 'backoffice/report_pages/external_material/external_report_list.html', context)

@login_required(login_url = 'signin')
@pic_only
def ExternalMaterialReportListView_PIC(request):
    project = Project.objects.filter(pic=request.user)
    data = ExternalMaterialReport.objects.filter(project__in=project).order_by('-date')
    context = {'data':data}
    return render(request, 'backoffice/report_pages/external_material/external_report_list.html', context)

@login_required(login_url = 'signin')
@whm_only
def ExternalMaterialReportListView_WHM(request):
    project = Project.objects.filter(whm=request.user)
    data = ExternalMaterialReport.objects.filter(project__in=project).order_by('-date')
    context = {'data':data}
    return render(request, 'backoffice/report_pages/external_material/external_report_list.html', context)


@login_required(login_url = 'signin')
@staff_only
def ExternalMaterialReportDetailView(request, pk):
    try:
        data = ExternalMaterialReport.objects.get(id=pk)
        data2 = ExternalMaterialReportDetails.objects.filter(report=data.id)
        context={'data':data, 'data2':data2}
        return render(request, 'backoffice/report_pages/external_material/external_report_detail.html', context)
    except ObjectDoesNotExist:
        return render(request, "404.html")

@login_required(login_url = 'signin')
@admin_only
def ExternalMaterialReportDeleteView(request, pk):
    data = ExternalMaterialReport.objects.get(id=pk)
    data2 = ExternalMaterialReportDetails.objects.filter(report=data.id)
    if request.method == "POST":
        data.delete()
        messages.success(request, "Material Report has been deleted.")
        group = request.user.groups.all()[0].name
        if group == "Admin":
            return redirect('materialreport_list')
        elif group == "Warehouseman":
            return redirect('materialreport_list_whm')
        return redirect('materialreport_list')
    context={'data':data, 'data2':data2}
    return render(request, 'backoffice/report_pages/external_external_material/external_report_delete.html', context)
#################################################################################################################################
#################################################################################################################################
@login_required(login_url = 'signin')
@admin_only
def LandingPageImageCreateView(request):
    data2 = LandingPageTitle.objects.all().order_by('name', 'category')
    if request.method == "POST":
        form = LandingPageTitleForm(request.POST)
        form2  = LandingPageImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        if form.is_valid() and form2.is_valid():
            data = form.save()
            form2.save(commit=False)
            for f in files:
                image = LandingPageImage(title=data, image=f)
                image.save()
            messages.success(request, "Landing Page Image has been save.")
            return redirect('landing_page_create')
    else:
        form = LandingPageTitleForm()
        form2 = LandingPageImageForm()
    context = {'form':form, 'form2':form2, 'data2':data2}
    return render(request, 'backoffice/landing_pages/landing_page_create.html', context)

@login_required(login_url = 'signin')
@admin_only
def LandingPageImageDetailView(request, pk):
    data = LandingPageTitle.objects.get(id=pk)
    data2 = LandingPageImage.objects.filter(title=data)
    context = {'data':data, 'data2':data2}
    return render(request, 'backoffice/landing_pages/landing_page_detail.html', context)

@login_required(login_url = 'signin')
@admin_only
def LandingPageImageUpdateView(request, pk):
    data = LandingPageTitle.objects.get(id=pk)
    if request.method == 'POST':
        formset  = LandingPageImageFormset(request.POST, request.FILES, instance=data)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Landing Page Image has been Update.")
            return redirect('landing_page_create')
    else:
        formset = LandingPageImageFormset(instance=data)
    context = {'formset':formset, 'data':data,}
    return render(request, 'backoffice/landing_pages/landing_page_update.html', context)   

@login_required(login_url = 'signin')
@admin_only
def LandingPageImageDeleteView(request, pk):
    data = LandingPageTitle.objects.get(id=pk)
    data2 = LandingPageImage.objects.filter(title=data)
    if request.method == "POST":
        data.delete()
        messages.success(request, "Landing Page Image has been deleted")
        return redirect('landing_page_create')
    context = {'data':data, 'data2':data2}
    return render(request, 'backoffice/landing_pages/landing_page_delete.html', context)

#################################################################################################################################
#################################################################################################################################
@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Client'])
def Client_home(request):
    client = request.user.id
    data = Project.objects.filter(client=client)
    context = {'data':data}
    return render(request, 'client/client-home.html', context)

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Client'])
def ClientProjectView(request,pk):
    try:
        data = Project.objects.get(id=pk)
        blueprint = ProjectBlueprint.objects.filter(project_id=data.id)
        data2 = Quotation.objects.filter(project_id=data.id)
        data5 = SitePhotos.objects.filter(project_id=data.id)
        rework = Rework.objects.filter(project_id=data.id)
        try:
            data3 = ProjectProgress.objects.get(project_id=data.id)
            data4 = ProjectProgressDetails.objects.filter(projectprogress=data3.id)
        except ObjectDoesNotExist:
            context = {'data':data, 'data2':data2, 'data5':data5, 'blueprint':blueprint, 'rework':rework}
            return render(request, 'client/client-view_project.html', context)
        context={'data':data, 'data2':data2, 'data3':data3, 'data4':data4, 'data5':data5, 'blueprint':blueprint}
        return render(request, 'client/client-view_project.html', context)
    except ObjectDoesNotExist:
        return render(request, "404.html")
    
@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Client'])
def ClientSitePhotosView(request, pk):
    try:
        data = SitePhotos.objects.get(id=pk)
        data2 = SitePhotosDetails.objects.filter(sitephotos=data, reveal="True")
        context={'data':data, 'data2':data2}
        return render(request, 'client/client-sitephotos.html', context)
    except ObjectDoesNotExist:
        return render(request, "404.html")

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Client'])
def ClientQuotationView(request,pk):
    try:
        data = Quotation.objects.get(id=pk)
        project = Project.objects.get(id=data.project.id)
        if project.client != request.user:
            return redirect('client_quotation')
        data2 = QuotationDetails.objects.filter(quotation=data.id)
        if request.method == "POST":
            data.status = request.POST.get("status")
            data.save()
            if data.status == "Accepted":
                admin = User.objects.filter(groups__name="Admin")
                for i in admin:
                    adnin_notif = Notification.objects.create(receiver=i, description=f"{project.client} has accepted the quotation on project {project.project}", url=f"/project/quotation/{data.id}")
                pm_notif =  Notification.objects.create(receiver=project.pm, description=f"{project.client} has accepted the quotation on project {project.project}", url=f"/project/quotation/{data.id}")
                messages.success(request, "Quotation has been accepted.")
            else:
                admin = User.objects.filter(groups__name="Admin")
                for i in admin:
                    adnin_notif = Notification.objects.create(receiver=i, description=f"{project.client} has rejected the quotation on project {project.project}", url=f"/project/quotation/{data.id}")
                pm_notif =  Notification.objects.create(receiver=project.pm, description=f"{project.client} has rejected the quotation on project {project.project}", url=f"/project/quotation/{data.id}")
                messages.success(request, "Quotation has been rejected.")
            return redirect('client_home')
        context = {'data':data, 'data2':data2,}
        return render(request, 'client/client-quotation.html', context)
    except ObjectDoesNotExist:
        return render(request, "404.html")

@login_required(login_url = 'signin')
@allowed_users(allowed_roles = ['Client'])
def ClientReworkDetailView(request,pk):
    try:
        data = Rework.objects.get(id=pk)
        data2 = ReworkBeforeImage.objects.filter(rework=data.id)
        data3 = ReworkAfterImage.objects.filter(rework=data.id)
        context={'data':data, 'data2':data2, 'data3':data3,}
        return render(request, 'client/client-rework.html', context)
    except ObjectDoesNotExist:
        return render(request, "404.html")

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
            messages.success(request, ' Your Profile has been updated')
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
        messages.success(request, "Password has been changed.")
        return redirect('client_profile')
    context={'form':form,}
    return render(request, 'client/client-change_password.html', context)

#################################################################################################################################
#################################################################################################################################
@api_view(['POST'])
def InquiryCreate_api(request):
    serializer = InquirySerializers(data=request.data)
    if serializer.is_valid():
	    serializer.save()
    data = serializer.save()
    return Response(serializer.data) 

@login_required(login_url = 'signin')
@api_view(['GET'])
def Notification_api(request, pk):
    notification = Notification.objects.filter(receiver_id=pk, is_read=False).order_by('-timestamp')
    serializer = NotificationSerializers(notification, many=True)
    return Response(serializer.data)

@login_required(login_url = 'signin')
@api_view(['GET'])
def NotificationMarkAll_api(request, pk):
    notification = Notification.objects.filter(receiver_id=pk, is_read=False).order_by('-timestamp')
    for i in notification:
        i.delete()
    serializer = NotificationSerializers(notification, many=True)
    return Response(serializer.data)

@login_required(login_url = 'signin')
@api_view(['GET'])
def NotificationMark_api(request, pk):
    notification = Notification.objects.get(id=pk)
    notification.delete()
    serializer = NotificationSerializers(notification, many=False)
    return Response(serializer.data)

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

#################################################################################################################################
#################################################################################################################################
import os
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


def link_callback(uri, rel):
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
                result = [result]
        result = list(os.path.realpath(path) for path in result)
        path=result[0]
    else:
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        if uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        elif uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        else:
            return uri

    if not os.path.isfile(path):
        raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, link_callback=link_callback)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

class ProjectReport(FormView, LoginRequiredMixin):
    form_class = WeeklyReportForm
    template_name='backoffice/report_pages/projectreport_search.html'

    @method_decorator(no_whm, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    

class ProjectReportPDF(TemplateView, LoginRequiredMixin):
    login_url ="signin"
    redirect_field_name="redirect_to"
    
    def get(self, request, *args, **kwargs):
        project = self.request.GET.get('project')
        datefrom = self.request.GET.get('date_from')
        datefrom = datetime.datetime.strptime(datefrom, "%Y-%m-%d")
        dateto =  self.request.GET.get('date_to')
        dateto = datetime.datetime.strptime(dateto, "%Y-%m-%d")
        project = Project.objects.get(id=project)
        try:
            requisition = Requisition.objects.filter(project_id=project.id, date__range=[datefrom, dateto])
            requisitiondetails = RequisitionDelivery.objects.filter(requisition__in=requisition)
            externalorder = ExternalOrder.objects.filter(project_id=project.id, date__range=[datefrom, dateto])
            externalorder_details = ExternalOrderDetails.objects.filter(externalorder__in=externalorder)
            joborder = JobOrder.objects.filter(project_id=project.id, date__range=[datefrom, dateto])
            jobordertask = JobOrderTask.objects.filter(joborder__in=joborder)
            rework = Rework.objects.filter(project_id=project.id, date__range=[datefrom, dateto])
            sitephotos = SitePhotos.objects.filter(project_id=project.id, date__range=[datefrom, dateto])
            sitephotosdetails = SitePhotosDetails.objects.filter(sitephotos__in=sitephotos)
            projectissues = ProjectIssues.objects.filter(project_id=project.id, date__range=[datefrom, dateto])
            materialreport = MaterialReport.objects.filter(project_id=project.id, date__range=[datefrom, dateto])
            materialreportdetails = MaterialReportDetails.objects.filter(report__in=materialreport)
            externalmaterialreport = ExternalMaterialReport.objects.filter(project_id=project.id, date__range=[datefrom, dateto])
            externalmaterialreportdetails = ExternalMaterialReportDetails.objects.filter(report__in=externalmaterialreport)
            projectinventory = ProjectInventory.objects.get(project_id=project.id)
            projectinventorydetails = ProjectInventoryDetails.objects.filter(inventory_id=projectinventory.id)
            externalprojectinventory = ExternalProjectInventory.objects.get(project_id=project.id)
            externalprojectinventorydetails = ExternalProjectInventoryDetails.objects.filter(inventory_id=externalprojectinventory.id)
            data={
                'project':project, 'datefrom':datefrom, 'dateto':dateto,
                'requisition':requisition, 'requisitiondetails':requisitiondetails, 
                'externalorder':externalorder, 'externalorder_details':externalorder_details,
                'joborder':joborder, 'jobordertask':jobordertask,
                'rework':rework, 'projectissues':projectissues,
                'sitephotos':sitephotos, 'sitephotosdetails':sitephotosdetails,
                'materialreport':materialreport,'externalmaterialreport':externalmaterialreport,
                'materialreportdetails':materialreportdetails, 'externalmaterialreportdetails':externalmaterialreportdetails,
                'projectinventorydetails':projectinventorydetails, 'externalprojectinventorydetails': externalprojectinventorydetails,
                'projectinventory': projectinventory, 'externalprojectinventory':externalprojectinventory,
            }
            pdf = render_to_pdf('pdf_template.html', data)
            return HttpResponse(pdf, content_type='application/pdf')
        except ObjectDoesNotExist:
            messages.warning(request, "Input dates does not match on data or does not exist at all.")
            return redirect('projectreport')
		

# class DownloadPDF(View):
# 	def get(self, request, *args, **kwargs):
# 		pdf = render_to_pdf('pdf_template.html', data)
# 		response = HttpResponse(pdf, content_type='application/pdf')
# 		filename = "poliworks_%s.pdf" %("12341231")
# 		content = "attachment; filename='%s'" %(filename)
# 		response['Content-Disposition'] = content
# 		return response