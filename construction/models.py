from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import (AbstractBaseUser)
from django.contrib.auth.models import User, Group
from .managers import UserManager
from django.conf import settings
from django.db import models
from django.db.models import F, Sum
from decimal import Decimal

import djfractions
import datetime



def profile_upload_path(instance, filename):
    return 'profile_image/{0}/{1}'.format(instance.user, filename)

def estimate_upload_path(instance, filename):
    return 'Estimate/{}/{}'.format(instance.estimate.name, filename)

def project_upload_path(instance, filename):
    return 'Projects/{0}/blueprint~design/{1}'.format(instance.project, filename)

def project_sitephotos_path(instance, filename):
    return 'Projects/{0}/sitephotos/{1}'.format(instance.sitephotos.project, filename)

def or_upload_path(instance, filename):
    return 'Projects/{0}/or image/{1}'.format(instance.project, filename)

def requisition_upload_path(instance, filename):
    return 'Projects/{0}/requisition image/{1}'.format(instance.requisition.project, filename)

class Province(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        name ='%s' % (self.name)
        return name.strip()
    class Meta:    
        verbose_name_plural="Admin - Province"
        verbose_name = "Admin - Province"

class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    def __str__(self):
        name ='%s' % (self.name)
        return name.strip()
    class Meta:
        verbose_name_plural="Admin - City"
        
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    first_name = models.CharField(('First Name'),max_length=255, null=True)
    middle_name = models.CharField(('Middle Name'),max_length=255, blank=True, null=True)
    last_name = models.CharField(('Last Name'),max_length=255, null=True)
    suffix = models.CharField(('Suffix'),max_length=255, null=True, blank=True)
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 
    objects = UserManager()

    def full_name(self):
       full_name = '%s %s %s %s' % (self.first_name, self.middle_name, self.last_name, self.suffix)
       return full_name.strip()

    def get_short_name(self):
        name= '%s %s' % (self.first_name,self.last_name)
        return name.strip()

    def get_email(self):              
        return self.email

    def __str__(self):
        flname ='%s %s' % (self.first_name, self.last_name)
        return flname.strip()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True
    
    @property
    def staff(self):
        "Is the user a member of staff?"
        return self.is_staff

    @property
    def superuser(self):
        "Is the user a superuser?"
        return self.is_superuser

    @property
    def active(self):
        "Is the user active?"
        return self.is_active
    
    class Meta:
        verbose_name_plural = 'Admin - User'
        verbose_name = 'Admin - User'

class Gender(models.Model):
    gender = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural = 'Admin - Gender'

    def __str__(self):
        return self.gender

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default="user.png", upload_to=profile_upload_path)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    birthdate = models.DateField(('Birth date'), help_text='Format: yyyy-mm-dd', null=True) 
    phone = models.CharField(('Phone'),blank=True, help_text='Contact phone number', max_length=15)
    address = models.CharField(max_length=255, help_text='Apartment, suite, unit, building, floor, street, barangay')
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, verbose_name='Province', null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, verbose_name='City', null=True)
    class Meta:
        verbose_name='Profile'
        verbose_name_plural='Profile'
    def content_file_name(instance, filename):
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        filename = "%s_%s.%s" % (instance.user.id, suffix)
        return os.path.join('uploads', filename)
    def __str__(self):
        return str(self.user)

class ProjectType(models.Model):
    projecttype = models.CharField(max_length=255, null=True)
    class Meta:
        verbose_name_plural='Admin - Project Type'
    def __str__(self):
        return self.projecttype

class Inquiry(models.Model):
    name = models.CharField(('Name'),max_length=255)
    phone = models.CharField(('Contact Number'), max_length=20)
    email = models.CharField(('Email'), max_length=255)
    message = models.TextField(('Message'), null=True)
    date_created = models.DateTimeField(('Date Created'), auto_now_add=True)
    status = models.BooleanField(default=False)

class Estimate(models.Model):
    name = models.CharField(('Name'),max_length=255)
    phone = models.CharField(('Contact Number'), max_length=20)
    email = models.CharField(('Email'), max_length=255)
    call_time = models.CharField(('Best time to call'), max_length=255)
    typeofproject = models.ForeignKey(ProjectType, on_delete=models.SET_NULL, null=True, verbose_name='Project Type')
    address = models.CharField(max_length=255, null=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, verbose_name='Province', null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, verbose_name='City', null=True)
    lotarea = models.CharField(max_length=255, blank=True, verbose_name='Lot Area', help_text="Please indicate if square meter, hectare, acre")
    budget = models.FloatField(('Estimated Budget'), max_length=255)
    date_start = models.DateField(('Estimated Date Start'), null=True,)
    message = models.TextField(('Message'), null=True, blank=True)
    date_created = models.DateTimeField(('Date Created'), auto_now_add=True)
    status = models.BooleanField(default=False)

class EstimateImage(models.Model):
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE)
    image = models.FileField(verbose_name='Image/Design/Reference', upload_to=estimate_upload_path)

class Project(models.Model):
    project = models.CharField(('Project Name'),max_length=255, null=True)
    address = models.CharField(('Address'), max_length=255, null=True, help_text='Apartment, suite, unit, building, floor, street, barangay')
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, verbose_name='Province', null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, verbose_name='City', null=True)
    pm = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_pm', 
        verbose_name='Project Manager', limit_choices_to={'groups__name': "Project Manager"})
    pic = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,blank=True,
        related_name='project_pic', verbose_name='Person In Charge', limit_choices_to={'groups__name': "Person In-Charge"})
    whm = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,blank=True,
        related_name='project_whm', verbose_name='Warehouseman',limit_choices_to={'groups__name': "Warehouseman"})
    client = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, 
        related_name='project_client', verbose_name='Client',limit_choices_to={'groups__name': "Client"})
    status = {('Pending','Pending'),('On-going','On-going'),('Completed','Completed'),('Completed (Overdue)','Completed (Overdue)')}
    status = models.CharField(max_length=255, choices=status, blank=True ,default='Pending')
    typeofproject = models.ForeignKey(ProjectType, on_delete=models.SET_NULL, null=True, verbose_name='Project Type')
    lotarea = models.CharField(max_length=255, blank=True, verbose_name='Lot Area', 
        help_text="Please indicate if square meter, hectare, acre")
    startdate = models.DateField(('Start Project Date'),  help_text='Format: YYYY-MM-DD', blank=True,null=True)
    comdate = models.DateField(('Project Completion Date'), help_text='Format: YYYY-MM-DD', blank=True, null=True)
    mpd = models.DateField(('Maintenance Period End Date'), help_text='Format: YYYY-MM-DD', blank=True, null=True)
    design=models.ImageField(('Blueprint'),upload_to=project_upload_path, blank=True, null=True)
    class Meta:
        verbose_name='Project'
        verbose_name_plural='Project'
    def __str__(self):
        return self.project

class ScopeOfWorkCategory(models.Model):
    category = models.CharField(('Category'), max_length=255)
    class Meta:
        verbose_name_plural='Admin - Category(Scope of Work)'
        verbose_name='Admin - Category(Scope of Work)'
    def __str__(self):
        return self.category

class ScopeOfWork(models.Model):
    category = models.ForeignKey(ScopeOfWorkCategory, on_delete=models.CASCADE)
    scope = models.CharField(('Description'), max_length=255, null=True)
    materialcost = models.FloatField(('Material Cost'),blank=True)
    laborcost = models.FloatField(('Labor Cost'), blank=True)
    subbid = models.FloatField(('Sub bid'), blank=True)
    class Meta:
        verbose_name_plural='Admin - Scope Of Work'
        verbose_name='Admin - Scope Of Work'
    def get_cost(self):
        return self.materialcost+self.laborcost+self.subbid
    def get_scope(self):
        return self.scope
    def __str__(self):
        scope = '%s %s %s' % (self.scope," - ",self.materialcost+self.laborcost+self.subbid)
        return scope.strip()

class Quotation(models.Model):
    status_choice = {('Pending','Pending'),('Accepted','Accepted'),('Rejected','Rejected')}
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='quotation', verbose_name='Project')
    subject = models.CharField(('Subject'),max_length=255, null=True)
    date = models.DateField(('Date'),default=datetime.date.today)
    amount = models.FloatField(('Total Amount'), default=0)
    status = models.CharField(('Status'), max_length=255, default='Pending',choices=status_choice)
    class Meta:
        verbose_name = 'Project - Quotation'
        verbose_name_plural = 'Project - Quotation'
    def get_vat(self):
        vat = self.amount *.12
        return vat
    def get_grandtotal(self):
        grandtotal = self.amount + (self.amount*.12)
        return grandtotal
    def __str__(self):
        return "{0}".format(self.project)

class QuotationDetails(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    scope_of_work = models.ForeignKey(ScopeOfWork, on_delete=models.CASCADE, related_name='quotationsow', verbose_name='quotation')
    unit = models.CharField(max_length=255, blank=True)
    quantity = models.IntegerField(('Quantity'))
    def q_amount(self):
        return self.quantity*self.scope_of_work.get_cost()

class ProjectProgress(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    total_progress = models.FloatField(default=0)

class ProjectProgressDetails(models.Model):
    choice = {(1,'low'),(3,'medium'),(5,'high')}
    status_choice = {('Pending','Pending'),('On-going','On-going'),('Done','Done')}
    projectprogress = models.ForeignKey(ProjectProgress, on_delete=models.CASCADE )
    scope_of_work = models.CharField(max_length=255, verbose_name="Scope of Work")
    level = models.IntegerField(choices=choice,default=1, verbose_name="Level")
    status = models.CharField(max_length=255, default="Pending", choices=status_choice, verbose_name="Status")
    start_date = models.DateField(verbose_name="Start Date", null=True, blank=True)
    completion_date = models.DateField(verbose_name="Completion Date", null=True, blank=True)

class PersonnelSkill(models.Model):
    skill = models.CharField(('Skill'), max_length=255)
    class Meta:
        verbose_name_plural = 'Admin - Personnel Skills'
        verbose_name = 'Admin - Personnel Skills'
    def __str__(self):
        return self.skill
    def __unicode__(self):
        return self.skill

class PersonnelType(models.Model):
    personneltype = models.CharField(max_length=255, null=True, verbose_name="Type of Personnel")
    class Meta:
        verbose_name='Admin - Personnel Type'
        verbose_name_plural = 'Admin - Personnel Type'
    def __str__(self):
        return self.personneltype

class Personnel(models.Model):
    first_name = models.CharField(('First Name'), max_length=255)
    middle_name = models.CharField(('Middle Name'), max_length=255, blank=True, null=True)
    last_name = models.CharField(('Last Name'), max_length=255)
    suffix = models.CharField(('Suffix'), max_length=50, null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    contact = models.CharField(('Contact Number'), max_length=20)
    choice={('Company Worker', 'Company Worker'), ('Subcontractor','Subcontractor')}
    personnel_type = models.ForeignKey(PersonnelType, on_delete=models.SET_NULL, null=True)
    skill = models.ManyToManyField(PersonnelSkill, related_name='personnel')
    address = models.CharField(max_length=255, null=True, help_text='Apartment, suite, unit, building, floor, street, barangay')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, verbose_name='City', null=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, verbose_name='Province', null=True)
    status ={('Currently Assigned', 'Currently Assigned'), ('Available', 'Available')}
    status = models.CharField(('Status'), max_length=255, choices=status, default="Available")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    date2 = models.DateField(null=True, blank=True)
    class Meta:
        verbose_name_plural = 'Personnel'
        verbose_name = 'Personnel'
    def short_name(self):
       short_name = '%s %s' % (self.first_name, self.last_name)
       return short_name.strip()
    def __str__(self):
        flname ='%s %s' % (self.first_name, self.last_name)
        return flname.strip()

class JobOrder(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='joborder', verbose_name='Project')
    date = models.DateField(('Date Given'), help_text="Format: yyyy-mm-dd")
    duration = models.DateField(('Duration'), help_text="Format: yyyy-mm-dd")
    pic = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='joborder_pic', verbose_name='Prepared by', 
        limit_choices_to={'groups__name': "Person In-Charge"})
    class Meta:
        verbose_name = 'Project - Job Order'
        verbose_name_plural = 'Project - Job Order'
    def __str__(self):
        return self.project.__str__()

class JobOrderTask(models.Model):
    joborder = models.ForeignKey(JobOrder, on_delete=models.CASCADE, related_name='jobordertask', verbose_name='Joborder')
    personnel = models.ForeignKey(Personnel,on_delete=models.CASCADE, related_name='jobordertask', verbose_name='Personnel')
    activity = models.CharField(('Activity of the Week'), max_length=255)
    date = models.DateField(('From'), blank=True, null=True)
    date2 = models.DateField(('To'), blank=True, null=True)
    remarks = models.CharField(('Remarks'), max_length=255, blank=True, null=True)
    status = {('Pending','Pending'),('On-going','On-going'),('Done','Done')}
    status = models.CharField(('Status'), max_length=255, choices=status, default="Pending")
    completion_date = models.DateField(null=True, blank=True)
    class Meta:
        verbose_name = 'Job Order Task'
        verbose_name_plural = 'Job Order Tasks'
    def __str__(self):
        return self.activity

class Rework(models.Model):
    project=models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reworkform', verbose_name='Project')
    date=models.DateField(('Date'), default=datetime.date.today)
    subject=models.CharField(('Subject'), max_length=255)
    instruction=models.TextField()
    pm=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rework_pm', verbose_name='Prepared by', 
        limit_choices_to={'groups__name': "Project Manager"})
    class Meta:
        verbose_name_plural='Project - Rework'
        verbose_name='Project - Rework'


class Inventory(models.Model):
    alternate_code = models.CharField(verbose_name="Alternate Code", max_length=255, null=True, blank=True)
    item_code = models.CharField(verbose_name="Item Code", max_length=255, null=True, blank=True)
    unit = models.CharField(verbose_name="Unit", max_length=255, null=True, blank=True)
    description = models.CharField(verbose_name="Description", max_length=255)
    quantity = models.FloatField(verbose_name="Quantity", default=0)
    unit_price = models.FloatField(verbose_name="Unit Price", null=True, blank=True)
    class Meta:
        verbose_name_plural = 'Admin - Material Inventory Office'
    def __str__(self):
        return self.description 

class Requisition(models.Model):
    requisition_no= models.IntegerField(unique=True, null=True, verbose_name="requisition number")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='requisition_project',verbose_name='Project')
    date = models.DateField(default=datetime.date.today, verbose_name='Date')
    whm = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requisition_whm', verbose_name='Prepared by', 
        help_text="Warehouseman" ,limit_choices_to={'groups__name': "Warehouseman"})
    status = {('Pending', 'Pending'), ('To be Delivered', 'To be Delivered'),('Closed', 'Closed')}
    status = models.CharField( max_length=255, choices=status, default="Pending")
    class Meta:
        verbose_name_plural = 'Project - Requisition'
        verbose_name = 'Project - Requisition'


class RequisitionDetails(models.Model):
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, related_name='requisitiondetail', verbose_name='Requesition')
    articles = models.ForeignKey(Inventory, on_delete=models.CASCADE, verbose_name="Articles")
    quantity = models.IntegerField(('Request Quantity'),default=1)
    class Meta:
        verbose_name_plural = 'Requisition Details'
        verbose_name = 'Requisition Detail'

class RequisitionDelivery(models.Model):
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, verbose_name='Requesition')
    articles = models.ForeignKey(Inventory, on_delete=models.CASCADE, verbose_name="Articles")
    quantity = models.IntegerField(('Delivered Quantity'),default=0, null=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)
    status=(('Canceled', 'Canceled'),('To be delivered', 'To be delivered'))
    status = models.CharField(('Status'),max_length=255, choices=status, null=True,)
    status2 ={('Incomplete', 'Incomplete'), ('Not Received','Not Received'), ('Complete','Complete')}
    status2 = models.CharField(('Action'), max_length=255, choices=status2, null=True, blank=True)
    quantity2 = models.IntegerField(('Received Quantity'), null=True, blank=True, default=0)

class RequisitionImage(models.Model):
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE)
    image=models.FileField(upload_to=requisition_upload_path, verbose_name='Image', null=True, blank=True)
    class Meta:
        verbose_name_plural= "Requisition Image(dr/image proof)"
        verbose_name = "Requisition Image(dr/image proof)"


class ExternalOrder(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='externalorder_project', verbose_name='Project')
    supplier = models.CharField(max_length=255)
    date = models.DateField(default=datetime.date.today, verbose_name='Date')
    whm = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='externalorder_whm', verbose_name='Prepared By', 
        limit_choices_to={'groups__name': "Warehouseman"}, help_text="Warehouseman")
    amount = models.FloatField(verbose_name='Amount', default=0)
    image = models.ImageField(upload_to=or_upload_path, null=True, blank=True, verbose_name="OR Image")
    class Meta:
        verbose_name_plural = 'Project - External Order'
        verbose_name = 'Project - External Order'


class ExternalOrderDetails(models.Model):
    externalorder = models.ForeignKey(ExternalOrder, on_delete=models.CASCADE, related_name='externalorderdetails', verbose_name='Outside Purchase') 
    quantity = models.IntegerField((), default=1,)
    unit = models.CharField(('Unit'),max_length=255)
    articles = models.CharField(('Article'),max_length=255)
    unitprice = models.FloatField(('Unit Price'))
    class Meta:
        verbose_name_plural='External Order Details'
        verbose_name='External Order Detail'
    def get_total(self):
        return self.quantity * self.unitprice
    

class ProjectIssues(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projectissue')
    date = models.DateField(default=datetime.date.today)
    description = models.TextField()
    whm=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projectissue_whm', verbose_name='Prepared by:', 
        help_text='Warehouseman',limit_choices_to={'groups__name': "Warehouseman",})
    class Meta:
        verbose_name='Project Issue'
        verbose_name_plural='Project Issues'
    def __str__(self):
        return self.date
    def get_problem(self):
        return self.problem
    def get_project(self):
        return self.project
    class Meta:
        verbose_name = "Project - Project Issues"
        verbose_name_plural = "Project - Project Issues"
    

class SitePhotos(models.Model):
    project=models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    date=models.DateField(default=datetime.date.today)
    class Meta:
        verbose_name = 'Project - SitePhotos'
        verbose_name_plural = 'Project - SitePhotos'
    def __str__(self):
        return self.project


class SitePhotosDetails(models.Model):
    sitephotos = models.ForeignKey(SitePhotos, on_delete=models.CASCADE, null=True)
    image=models.FileField(upload_to=project_sitephotos_path, verbose_name='Photos')
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    reveal=models.BooleanField(("Let the client view this?"), choices=BOOL_CHOICES, default=False, null=True)
    class Meta:
        verbose_name_plural='Site Photos'
        verbose_name='Site Photos'


class ProjectInventory(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE,verbose_name='Project')
    last_update = models.DateField(auto_now=True)
    class Meta:
        verbose_name_plural='Project - Inventory(onsite)'
        verbose_name='Project - Inventory(onsite)'
    

class ProjectInventoryDetails(models.Model):
    inventory = models.ForeignKey(ProjectInventory, on_delete=models.CASCADE, verbose_name='Project Inventory')
    articles = models.ForeignKey(Inventory, on_delete=models.CASCADE, verbose_name="Articles")
    quantity = models.IntegerField(('Quantity'), null=True, blank=True)
    def __str__(self):
        return self.articles.__str__()


class ProjectDailyReport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    whm = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,blank=True,
        related_name='dailyreport_whm', verbose_name='Warehouseman',limit_choices_to={'groups__name': "Warehouseman"})
    date = models.DateField(default=datetime.date.today)
    class Meta:
        verbose_name = 'Project - Material Report(Inventory - onsite)'
        verbose_name_plural = 'Project - Material Report(Inventory - onsite)'

class ProjectDailyReportDetails(models.Model):
    report = models.ForeignKey(ProjectDailyReport, on_delete=models.CASCADE, null=True)
    articles = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(null=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)


class ExternalProjectInventory(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, verbose_name='Project')
    last_update = models.DateField(auto_now=True)
    class Meta:
        verbose_name_plural='Project - External Inventory(onsite)'
        verbose_name='Project - External Inventory(onsite)'
    

class ExternalProjectInventoryDetails(models.Model):
    inventory = models.ForeignKey(ExternalProjectInventory, on_delete=models.CASCADE, verbose_name='Project Inventory')
    articles = models.CharField(max_length=255, null=True, blank=True)
    unit = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(('Quantity'), null=True, blank=True)
    def __str__(self):
        return self.articles


class ExternalOrderReport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    whm = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,blank=True,
        verbose_name='Warehouseman',limit_choices_to={'groups__name': "Warehouseman"})
    date = models.DateField(default=datetime.date.today)
    class Meta:
        verbose_name = 'Project - Material Report(External Inventory - onsite)'
        verbose_name_plural = 'Project - Material Report(External Inventory - onsite)'

class ExternalOrderDetailsReport(models.Model):
    report = models.ForeignKey(ExternalOrderReport, on_delete=models.CASCADE, null=True)
    articles = models.ForeignKey(ExternalProjectInventoryDetails, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    remarks = models.CharField(max_length=255, null=True, blank=True)

