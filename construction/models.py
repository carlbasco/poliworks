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

def project_upload_path(instance, filename):
    return 'Projects/{0}/{1}'.format(instance.ProjectSite, filename)

# class ZipCode(models.Model):
#     location = models.CharField(max_length=255)
#     city = models.CharField(max_length=255)
#     zipcode = models.IntegerField()
#     def __str__(self):
#         address='%s %s %s %s %s '%(self.location, ', ',self.city,' - ',self.zipcode)
#         return address.strip()
#     class Meta:
#         verbose_name_plural='Location'
#         ordering = ['location']

class Province(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        name ='%s' % (self.name)
        return name.strip()
    verbose_name_plural="Province"

class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    def __str__(self):
        name ='%s' % (self.name)
        return name.strip()
    class Meta:
        verbose_name_plural="Cities"
        
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    first_name = models.CharField(('First Name'),max_length=255, null=True)
    middle_name = models.CharField(('Middle Name'),max_length=255,blank=True)
    last_name = models.CharField(('Last Name'),max_length=255, null=True)
    suffix = models.CharField(('Suffix'),max_length=255, blank=True)
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

class Profile(models.Model):
    choices = (('Male', 'Male'),('Female', 'Female'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default="user.png", upload_to=profile_upload_path)
    sex = models.CharField(('Sex'),max_length=10, choices=choices)
    birthdate = models.DateField(('Birth date'), help_text='Format: yyyy-mm-dd', null=True) 
    phone = models.CharField(('Phone'),blank=True, help_text='Contact phone number', max_length=15)
    address = models.CharField(max_length=255, blank=True, help_text='Apartment, suite, unit, building, floor, street, barangay')
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, verbose_name='Province', null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, verbose_name='City', null=True)
    # zipcode = models.ForeignKey(ZipCode, on_delete=models.DO_NOTHING, help_text='Barangay/City/Zipcode',verbose_name='Location')
    class Meta:
        verbose_name='Profile'
        verbose_name_plural='Profile'

    def content_file_name(instance, filename):
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        filename = "%s_%s.%s" % (instance.user.id, suffix)
        return os.path.join('uploads', filename)
    
    def __str__(self):
        return str(self.user)

class ProjectSite(models.Model):
    projectsite = models.CharField(('Project Name'),max_length=255, null=True)
    address = models.CharField(('Address'), max_length=255, null=True, help_text='Apartment, suite, unit, building, floor, street, barangay')
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, verbose_name='Province', null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, verbose_name='City', null=True)
    pm = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projectsite_pm', 
        verbose_name='Project Manager', limit_choices_to={'groups__name': "Project Manager"})
    pic = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,blank=True,
        related_name='projectsite_pic', verbose_name='Person In Charge', limit_choices_to={'groups__name': "Person In-Charge"})
    whm = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,blank=True,
        related_name='projectsite_whm', verbose_name='Warehouseman',limit_choices_to={'groups__name': "Warehouseman"})
    client = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, 
        related_name='projectsite_client', verbose_name='Client',limit_choices_to={'groups__name': "Client"})
    status = {('Pending','Pending'),('On-going','On-going'),('Completed','Completed'),}
    status = models.CharField(max_length=255, choices=status, blank=True ,default='Pending')
    projecttype={
        ('General Construction','General Construction'),('Interior Fit-out Works','Interior Fit-outWorks'),
        ('Self-Leveling Floor Applcation','Self-Leveling Floor Applcation'),('Concrete Countertops', 'Concrete Countertops'),
        ('Industrial Cement Flooring Finish', 'Industrial Cement Flooring Finish'),
    }
    typeofproject = models.CharField(max_length=255, choices=projecttype, null=True, verbose_name='Project Type')
    lotarea = models.CharField(max_length=255, blank=True, verbose_name='Lot Area')
    startdate = models.DateField(('Start Project Date'),  help_text='Format: YYYY-MM-DD', blank=True)
    comdate = models.DateField(('Project Completion Date'), help_text='Format: YYYY-MM-DD', blank=True)
    mpd = models.DateField(('Maintenance Period End Date'), help_text='Format: YYYY-MM-DD', blank=True)
    # design=models.ImageField(upload_to='images/projectdesign/%Y/%m/%d/', blank=True)
    class Meta:
        verbose_name='Projects'
        verbose_name_plural='Projects'
    def __str__(self):
        return self.projectsite

class ScopeOfWorkCategory(models.Model):
    category = models.CharField(('Category'), max_length=255)
    class Meta:
        verbose_name_plural='Scope Of Work Categories'
        verbose_name='Scope Of Work'
    def __str__(self):
        return self.category

class ScopeOfWork(models.Model):
    category = models.ForeignKey(ScopeOfWorkCategory, on_delete=models.CASCADE)
    scope = models.CharField(('Description'), max_length=255, null=True)
    materialcost = models.FloatField(('Material Cost'),blank=True)
    laborcost = models.FloatField(('Labor Cost'), blank=True)
    subbid = models.FloatField(('Sub bid'), blank=True)
    class Meta:
        verbose_name_plural='Scope Of Works'
        verbose_name='Scope Of Work'
    
    def get_cost(self):
        return self.materialcost+self.laborcost+self.subbid

    def get_scope(self):
        return self.scope
    
    def __str__(self):
        return self.scope
        
class Quotation(models.Model):
    status_choice = {('Pending','Pending'),('Accepted','Accepted'),('Rejected','Rejected')}
    projectsite = models.ForeignKey(ProjectSite, on_delete=models.CASCADE, related_name='quotation', verbose_name='Project Site')
    subject = models.CharField(('Subject'),max_length=255, blank=True, null=True)
    date = models.DateField(('Date'),default=datetime.date.today)
    amount = models.FloatField(('Total Amount'), default=0)
    status = models.CharField(('Status'), max_length=255, default='Pending',choices=status_choice)
    class Meta:
        verbose_name = 'Quotation'
        verbose_name_plural = 'Quotations'
    
    def __str__(self):
        return "{0}".format(self.projectsite)

class QuotationDetails(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    scope_of_work = models.ForeignKey(ScopeOfWork, on_delete=models.CASCADE, related_name='quotationsow', verbose_name='quotation')
    unit = models.CharField(max_length=255, blank=True)
    quantity = models.IntegerField(('Quantity'))
    # cost = models.FloatField()

    def unitcost(self):
        return self.quantity*self.scope_of_work.get_cost()

class ProjectProgress(models.Model):
    projectsite = models.OneToOneField(ProjectSite, on_delete=models.CASCADE)
    total_progress = models.FloatField(default=0)

class ProjectProgressDetails(models.Model):
    choice = {(1,'low'),(3,'medium'),(5,'high')}
    status_choice = {('Pending','Pending'),('On-going','On-going'),('Done','Done')}
    projectprogress = models.ForeignKey(ProjectProgress, on_delete=models.CASCADE )
    scope_of_work = models.CharField(max_length=255, verbose_name="Scope of Work")
    level = models.IntegerField(choices=choice,default=1, verbose_name="Level")
    status = models.CharField(max_length=255, default="Pending", choices=status_choice, verbose_name="Status")

class PersonnelSkill(models.Model):
    skill = models.CharField(('Skill'), max_length=255)
    class Meta:
        verbose_name_plural = 'Personnel Skills'
        verbose_name = 'Personnel Skills'
        
    def __str__(self):
        return self.skill

class Personnel(models.Model):
    first_name = models.CharField(('First Name'), max_length=255)
    middle_name = models.CharField(('Middle Name'), max_length=255, blank=True)
    last_name = models.CharField(('Last Nane'), max_length=255)
    suffix = models.CharField(('Suffix'), max_length=50, blank=True)
    contact = models.CharField(('Contach Number'), max_length=20)
    skill = models.ForeignKey(PersonnelSkill, on_delete=models.CASCADE, related_name='personnel')
    choice={('Company Worker', 'Company Worker'), ('Subcontractor','Subcontractor')}
    personnel_type = models.CharField(('Type of Personnel'),max_length=255, choices=choice)
    class Meta:
        verbose_name_plural = 'Personnel'
        verbose_name = 'Personnel'

    def full_name(self):
       full_name = '%s %s %s %s' % (self.first_name, self.middle_name, self.last_name, self.suffix)
       return full_name.strip()
    
    def __str__(self):
        flname ='%s %s' % (self.first_name, self.last_name)
        return flname.strip()

class JobOrder(models.Model):
    projectsite = models.ForeignKey(ProjectSite, on_delete=models.CASCADE, related_name='joborder', verbose_name='Project Site')
    date = models.DateField(('Date Given'))
    duration = models.DateField(('Duration'))
    pic = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='joborder_pic', verbose_name='Prepared by', 
        limit_choices_to={'groups__name': "Person In-Charge"})
    whm = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='joborder_whm', verbose_name='Send to', 
        limit_choices_to={'groups__name': "Warehouseman"})
    class Meta:
        verbose_name = 'Job Order'
        verbose_name_plural = 'Job Orders'

class JobOrderTask(models.Model):
    joborder = models.ForeignKey(JobOrder, on_delete=models.CASCADE, related_name='jobordertask', verbose_name='Joborder')
    personnel = models.ForeignKey(Personnel,on_delete=models.CASCADE, related_name='jobordertask', verbose_name='Personnel')
    activity = models.CharField(('Activity of the Week'), max_length=255)
    duration = models.CharField(('Duration'), max_length=255, blank=True, null=True)
    class Meta:
        verbose_name = 'Job Order Task'
        verbose_name_plural = 'Job Order Tasks'

class Rework(models.Model):
    projectsite=models.ForeignKey(ProjectSite, on_delete=models.CASCADE, related_name='reworkform', verbose_name='Project Site')
    date=models.DateField(('Date'), default=datetime.date.today)
    subject=models.CharField(('Subject'), max_length=255)
    instruction=models.TextField()
    pic=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rework_pic', verbose_name='Person In-Charge', 
        limit_choices_to={'groups__name': "Person In-Charge"})
    pm=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rework_pm', verbose_name='Project Manager', 
        limit_choices_to={'groups__name': "Project Manager"})
    class Meta:
        verbose_name_plural='Rework Form'
        verbose_name='Rework Form'

# class ReworkDetails(models.Model):
#     rework=models.ForeignKey(Rework, on_delete=models.CASCADE, related_name='instruction', verbose_name='Rework Form')
#     instruction=models.TextField()
#     class Meta:
#         verbose_name_plural='Rework Form Details'
#         verbose_name='Rework Form Details'



class Inventory(models.Model):
    alternate_code = models.CharField(verbose_name="Alternate Code", max_length=255, null=True, blank=True)
    item_code = models.CharField(verbose_name="Item Code", max_length=255, null=True, blank=True)
    unit = models.CharField(verbose_name="Unit", max_length=255, null=True, blank=True)
    description = models.CharField(verbose_name="Description", max_length=255)
    quantity = models.FloatField(verbose_name="Quantity", default=0)
    unit_price = models.FloatField(verbose_name="Unit Price", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Inventory Office'

    def __str__(self):
        return self.description


class Requisition(models.Model):
    projectsite = models.ForeignKey(ProjectSite, on_delete=models.CASCADE, related_name='requisition_project',verbose_name='Project Site')
    date = models.DateField(default=datetime.date.today, verbose_name='Date')
    whm = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requisition_whm', verbose_name='Prepared by', 
        help_text="Warehouseman" ,limit_choices_to={'groups__name': "Warehouseman"})
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requisition_admin', verbose_name='Send To?', 
        help_text="Admin" ,limit_choices_to={'groups__name': "Admin"})
    class Meta:
        verbose_name_plural = 'Requisition Form'
        verbose_name = 'Requisition Form'
    
class RequisitionDetails(models.Model):
    status=(('Pending', 'Pending'),('Canceled', 'Canceled'),('Purchased', 'Purchased'),('Delivered', 'Delivered'))
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, related_name='requisitiondetail', verbose_name='Requesition')
    articles = models.ForeignKey(Inventory, on_delete=models.CASCADE, verbose_name="Articles")
    quantity = models.IntegerField(('Quantity'),default=1)
    # unit = models.CharField(('Unit'),max_length=255)
    status = models.CharField(('Status'),max_length=255, choices=status, default='Pending')
    class Meta:
        verbose_name_plural='Requisition Form Details'
        verbose_name='Requisition Form Detail'

class ExternalOrder(models.Model):
    projectsite = models.ForeignKey(ProjectSite, on_delete=models.CASCADE, related_name='externalorder_project',verbose_name='Project Site')
    supplier = models.CharField(max_length=255)
    date = models.DateField(default=datetime.date.today, verbose_name='Date')
    whm = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='externalorder_whm', verbose_name='Prepared By', 
        limit_choices_to={'groups__name': "Warehouseman"})
    amount = models.FloatField(verbose_name='Amount', default=0)
    class Meta:
        verbose_name_plural = 'Outside Purchases'
        verbose_name = 'Outside Purchase'

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

class WeeklyStatusReport(models.Model):
    projectsite=models.ForeignKey(ProjectSite, on_delete=models.CASCADE)
    dategiven=models.DateField(('Date Given'))
    duration=models.DateField(('Duration'))
    pic=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wsr_pic', verbose_name='Project In-Charge', limit_choices_to={'groups__name': "Project In-Charge"})
    class Meta:
        verbose_name_plural='Weekly Status Report'
        verbose_name='Weekly Status Report'

class ProjectStatus(models.Model):
    reference=models.ForeignKey(WeeklyStatusReport, on_delete=models.CASCADE, related_name='projectstatus') 
    status=models.CharField(max_length=255, blank=True)
    target=models.CharField(max_length=255, blank=True)
    class Meta:
        verbose_name_plural='Project Status'
        verbose_name='Project Status'

class SitePhotos(models.Model):
    reference=models.ForeignKey(WeeklyStatusReport, on_delete=models.CASCADE, related_name='sitephotos')
    photos=models.FileField(upload_to=project_upload_path, verbose_name='Photos')
    date=models.DateField(default=datetime.date.today)
    class Meta:
        verbose_name_plural='Site Photos'
        verbose_name='Site Photos'

class Manpower(models.Model):
    reference=models.ForeignKey(WeeklyStatusReport, on_delete=models.CASCADE, related_name='manpower')
    quantity=models.IntegerField(('Quantity'), default=1)
    manpower=models.CharField(('Man Power'),max_length=255)
    class Meta:
        verbose_name_plural='Man Power'
        verbose_name='Man Power'
    
class ProjectIssues(models.Model):
    projectsite=models.ForeignKey(ProjectSite, on_delete=models.CASCADE, related_name='projectissue')
    date=models.DateField(default=datetime.date.today)
    description=models.TextField()
    whm=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projectissue_whm', verbose_name='Prepared by:', 
        help_text='Warehouseman',limit_choices_to={'groups__name': "Warehouseman",})
    pic=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projectissue_pic', verbose_name='Send to: ', 
        help_text='Person In-Charge',limit_choices_to={'groups__name': "Person In-Charge"})
    class Meta:
        verbose_name='Project Issue'
        verbose_name_plural='Project Issues'
    def __str__(self):
        return self.date
    def get_problem(self):
        return self.problem
    def get_projectsite(self):
        return self.projectsite
    
class ProjectSolution(models.Model):
    reference=models.ForeignKey(WeeklyStatusReport, on_delete=models.CASCADE)
    problem=models.ForeignKey(
        ProjectIssues,
        on_delete=models.CASCADE,
        related_name='problem',
        verbose_name='projectissue')
    solution=models.TextField('Possible Solution')
    class Meta:
        verbose_name_plural='Issues'
        verbose_name='Issues'

class RequestForTheWeek(models.Model):
    reference=models.ForeignKey(WeeklyStatusReport, on_delete=models.CASCADE, related_name='requestfortheweek')
    date=models.DateField(('Date'))
    quantity=models.IntegerField(('Quantity'), blank=True)
    unit=models.CharField(('Unit'), max_length=255, blank=True)
    request=models.CharField(('Request'), max_length=255)
    class Meta:
        verbose_name_plural='Request for the Next Week'
        verbose_name='Request for the Next Week'
        
class DailyReport(models.Model):
    projectsite=models.ForeignKey(ProjectSite, on_delete=models.CASCADE)
    image=models.FileField(upload_to=project_upload_path, verbose_name='Photos')
    date=models.DateField(default=datetime.date.today)
    class Meta:
        verbose_name_plural='Site Photos'
        verbose_name='Site Photos'



