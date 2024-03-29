from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms.models import inlineformset_factory, formset_factory
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.auth.models import Group
from django import forms
from .models import *



class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password1 field with admin's
    password1 hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]

class SignupForm(forms.ModelForm):
    account = forms.ModelChoiceField(label="Account Type", queryset=Group.objects.all())
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    cpassword = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email','first_name','middle_name','last_name','suffix']

    def clean(self):
        account = self.cleaned_data.get('account')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_cpassword(self):
        password = self.cleaned_data.get("password")
        cpassword = self.cleaned_data.get("cpassword")
        if password and cpassword and password != cpassword:
            raise forms.ValidationError("Passwords don't match")
        return cpassword
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        exclude = ('datetime', 'status')
        
class EstimateForm(forms.ModelForm):
    class Meta:
        model = Estimate
        exclude =('datetime', 'status')
        widgets={
            'name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}),
            'phone' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Contact Number'}),
            'email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
            'call_time' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Best time to call'}),
            'typeofproject' : forms.Select(attrs={'class':'form-control', 'placeholder':'Type of Project'}),
            'address' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Location of Property'}),
            'lotarea' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Lot Area'}),
            'date_start':forms.DateInput( attrs={'class':'form-control dateinput', 'placeholder':'Estimated Date Start'}),
            'budget' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Estimate Budget (php)','min':0, "oninput":"validity.valid||(value='');"}),
            'message' : forms.Textarea(attrs={'class':'form-control', 'placeholder':'Message', 'style':'resize: none;'}),
        }
class EstimateImageForm(forms.ModelForm):
    class Meta:
        model = EstimateImage
        exclude = ('estimate',)
        widgets={
            'image' : forms.FileInput(attrs={'class':'custom-file-input', 'multiple': True, 'required':False})
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=('user',)

class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput, required=False)
    class Meta:
        model=Profile
        exclude=('user',)
        
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','middle_name','last_name','suffix']

    def save(self, commit=True):
        user = super(UserEditForm, self).save(commit=False)
        user.save()
        return user

#################################################################################################################################
#################################################################################################################################
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('whm', 'pic')
        widgets={
            'design' : forms.FileInput(attrs={'class':'custom-file-input'})
        }

class ProjectNewForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('whm', 'pic')

class ProjectBlueprintForm(forms.ModelForm):
    class Meta:
        model = ProjectBlueprint
        fields = ('image',)
        widgets={
            'image':forms.FileInput(attrs={'class':'custom-file-input','multiple': True, })
        }

ProjectBlueprintFormset = inlineformset_factory(Project, ProjectBlueprint,
    form = ProjectNewForm,
    exclude = ('project', 'address', 'province', 'city', 'pm', 'pic', 'whm', 'client', 'status', 'typeofproject', 'lotarea', 'startdate', 'comdate', 'mpd', 'design'),
    extra=1,
    can_delete=True,
)

class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('pm', 'client')
        widgets={
            'design' : forms.FileInput(attrs={'class':'custom-file-input'})
        }

class ProjectUpdateStaffForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('whm', 'pic')
        
class ProjectViewForm(forms.ModelForm):
    class Meta:
        model=Project
        fields='__all__'

        def __init__(self, *args, **kwargs):
            super(ProjectViewForm, self).__init__(*args, **kwargs)
            for key in self.fields.keys():
                self.fields[key].widget.attrs['readonly'] = True

#################################################################################################################################
#################################################################################################################################
class QuotationForm(forms.ModelForm):
    class Meta:
        model=Quotation
        fields='__all__'
        exclude = ('status','amount')
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(pm=user)

class QuotationNewForm(forms.ModelForm):
    scope_of_work = forms.ModelChoiceField(queryset=ScopeOfWork.objects.all(), widget=forms.Select(attrs={'class':'sow', 'required':True}))
    class Meta:
        model=Quotation
        fields='__all__'
        exclude = ('total',)

class QuotationFormAdmin(forms.ModelForm):
    class Meta:
        model=Quotation
        fields='__all__'
        
QuotationFormSet = inlineformset_factory(Quotation, QuotationDetails,
    form=QuotationNewForm,
    extra=1,
    can_delete=True,
    widgets={
        'unit':forms.TextInput(attrs={'class':'form-control',}),
        'quantity':forms.NumberInput( attrs={'class':'form-control qty','required': True, 'min':0, "oninput":"validity.valid||(value='');"}),
        'amount':forms.NumberInput(attrs={'class':'form-control amount','readonly': True}),
        'unit_cost':forms.NumberInput(attrs={'class':'form-control unit_cost','readonly':True}),
    }
)
#################################################################################################################################
#################################################################################################################################
class ProgressForm(forms.ModelForm):
    class Meta:
        model=ProjectProgress
        exclude=('total_progress', 'completion_date', )

ProgressFormset = inlineformset_factory(ProjectProgress, ProjectProgressDetails,
    form=ProgressForm,
    extra=0,
    can_delete=False,
    fields=('status','level'),
    exclude=('id',),
    widgets={
        'scope_of_work':forms.Select(attrs={'class':'form-control scope'}),
        'status':forms.Select(attrs={'class':'form-control'}),
        'level':forms.Select(attrs={'class':'form-control'}),
    }
)
#################################################################################################################################
#################################################################################################################################
class ClientQuotationForm(forms.ModelForm):
    class Meta:
        model=Quotation
        fields=('status',)
#################################################################################################################################
#################################################################################################################################        
class RequisitionForm(forms.ModelForm):
    class Meta:
        model=Requisition
        fields = '__all__'
        exclude = ('status', 'requisition_no', 'amount')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RequisitionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['project'].queryset = Project.objects.filter(whm=user)

class RequisitionAdminForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = '__all__'

class RequisitionNewForm(forms.ModelForm):
    unit = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control unit','readonly':'true', 'required':'false'}))
    articles = forms.ModelChoiceField(queryset=Inventory.objects.all(), widget=forms.Select(attrs={'class':'form-control art', 'required':True}))
    class Meta:
        model = Requisition
        fields ='__all__'

RequisitionFormSet = inlineformset_factory(Requisition, RequisitionDetails, 
    form = RequisitionNewForm, 
    extra = 1,
    can_delete = True,
    exclude = ('status', 'status2', 'quantity2', 'requisition_no', 'amount'),
    widgets={
        'quantity':forms.NumberInput(attrs={'class':'form-control', 'min':0, "oninput":"validity.valid||(value='');", 'required':True}),
    }
)
class RequisitionUpdateForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = '__all__'

RequisitionUpdateFormSet = inlineformset_factory(Requisition, RequisitionDetails, 
    form=RequisitionNewForm, 
    extra=0,
    can_delete=True,
    exclude = ('status', 'status2', 'quantity2', 'requisition_no', 'amount'),
    widgets={
        'quantity':forms.NumberInput(attrs={'class':'form-control', 'required':True, 'min':0, "oninput":"validity.valid||(value='');"}),
        'articles':forms.Select(attrs={'class':'form-control art'})
    }
)

class RequisitionPICForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = ('requisition_no',)
        widgets={
            'requisition_no':forms.TextInput(attrs={'class':'form-control'}),
        }

class RequisitionActionForm(forms.ModelForm):
    class Meta:
        model=Requisition
        fields='__all__'

class RequisitionImageForm(forms.ModelForm):
    class Meta:
        model = RequisitionImage
        fields = ('image',)
        widgets={
            'image':forms.FileInput(attrs={'class':'custom-file-input','multiple': True, 'required':True})
        }
        
RequisitionActionFormSet = inlineformset_factory(Requisition, RequisitionDelivery, 
    form=RequisitionActionForm, 
    exclude=('requisition','articles','quantity2', 'unit_price','total_price', 'unit'),
    extra=0,
    widgets={
        'remarks':forms.TextInput(attrs={'class':'form-control '}),
        'quantity':forms.TextInput(attrs={'class':'form-control', 'min':0, "oninput":"validity.valid||(value='');"}),
        'status':forms.Select(attrs={'class':'form-control', 'required':True}),
    }
)

RequisitionActionFormSet_whm = inlineformset_factory(Requisition, RequisitionDelivery, 
    form=RequisitionActionForm, 
    exclude=('requisition','quantity','articles','status','remarks', 'unit_price','total_price', 'unit'),
    extra=0,
    widgets={
        'status2':forms.Select(attrs={'class':'form-control status2', 'required':True}),
        'quantity2':forms.NumberInput(attrs={'class':'form-control qty2', 'min':0, "oninput":"validity.valid||(value='');"}),
    }
)
#################################################################################################################################
#################################################################################################################################
class ExternalOrderForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class':'custom-file-input','multiple': True, }))
    class Meta:
        model = ExternalOrder
        fields = '__all__'
        exclude = ('amount',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(whm=user)

class ExternalOrderNewForm(forms.ModelForm):
    totalprice = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control total_price','readonly':'true'}), required=False)
    class Meta:
        model = ExternalOrder
        fields='__all__'

class ExternalOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = ExternalOrder
        fields='__all__'

ExternalOrderFormSet = inlineformset_factory(ExternalOrder, ExternalOrderDetails,
    form=ExternalOrderNewForm,
    extra=1,
    can_delete=True,
    widgets={
        'quantity':forms.NumberInput(attrs={'class':'form-control','required': 'true'}),
        'unit':forms.TextInput(attrs={'class':'form-control', 'required':True}),
        'articles':forms.TextInput(attrs={'class':'form-control','required': 'true'}),
        'remarks':forms.TextInput(attrs={'class':'form-control'}),
        'unitprice':forms.NumberInput(attrs={'class':'form-control','required': 'true'})
    }    
)

ExternalOrderUpdateFormSet = inlineformset_factory(ExternalOrder, ExternalOrderDetails,
    form=ExternalOrderUpdateForm,
    extra=0,
    can_delete=True,
    widgets={
        'quantity':forms.NumberInput(attrs={'class':'form-control', 'required':True, 'min':0, "oninput":"validity.valid||(value='');"}),
        'unit':forms.TextInput(attrs={'class':'form-control', 'required':True}),
        'articles':forms.TextInput(attrs={'class':'form-control', 'required':True}),
        'unitprice':forms.NumberInput(attrs={'class':'form-control', 'required':True})
    }    
)
class ExternalMaterialReportForm(forms.ModelForm):
    class Meta:
        model = ExternalMaterialReport
        fields = '__all__'

ExternalMaterialReportFormSet = inlineformset_factory(ExternalMaterialReport, ExternalMaterialReportDetails,
    form=ExternalMaterialReportForm,
    extra=1,
    can_delete=True,
    widgets={
        'articles':forms.Select(attrs={'class':'form-control art', 'required':True}),
        'quantity':forms.NumberInput(attrs={'class':'form-control','required':True, 'min':0, "oninput":"validity.valid||(value='');"}),
        'remarks':forms.TextInput(attrs={'class':'form-control'}),
    }
)
#################################################################################################################################
#################################################################################################################################
class JobOrderForm(forms.ModelForm):
    class Meta:
        model=JobOrder
        fields='__all__'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(pic=user)

class JobOrderNewForm(forms.ModelForm):
    class Meta:
        model=JobOrder
        fields='__all__'

JobOrderFormSet = inlineformset_factory(JobOrder, JobOrderTask,
    form=JobOrderNewForm,
    exclude=('completion_date', 'status',),
    extra=1,
    can_delete=True,
    widgets={
        'personnel':forms.Select(attrs={'class':'form-control personnel', 'required':True}),
        'activity':forms.TextInput( attrs={'class':'form-control', 'required':True}),
        'date':forms.DateInput( attrs={'class':'form-control dateinput', 'required':True}),
        'date2':forms.DateInput( attrs={'class':'form-control dateinput', 'required':True}),
        'remarks':forms.TextInput( attrs={'class':'form-control'}),
    }  
)

class JobOrderUpdateForm(forms.ModelForm):
    class Meta:
        model=JobOrder
        fields='__all__'
        
class JobOrderTasksForm(forms.ModelForm):
    class Meta:
        model=JobOrderTask
        fields='__all__'

class JobOrderReportForm(forms.ModelForm):
    class Meta:
        model = JobOrder
        fields = '__all__'

JobOrderReportFormSet = inlineformset_factory(JobOrder, JobOrderTask,
    form=JobOrderReportForm,
    exclude=('activity', 'date','date2','personnel','completion_date','remarks'),
    extra=0,
    can_delete=False,
    widgets={
        'status':forms.Select(attrs={'class':'form-control'}),
    }  
)

#################################################################################################################################
#################################################################################################################################
class ReworkForm(forms.ModelForm):
    class Meta:
        model=Rework
        fields='__all__'
        
class ReworkBeforeImageForm(forms.ModelForm):
    class Meta:
        model = ReworkBeforeImage
        fields = ('image',)

ReworkBeforeFormset = inlineformset_factory(Rework, ReworkBeforeImage,
    form = ReworkBeforeImageForm,
    exclude = ('rework',),
    extra = 1,
    can_delete=True,
)

class ReworkAfterImageForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class':'custom-file-input','multiple': True, }))
    class Meta:
        model = ReworkAfterImage
        fields = ('image',)

class ReworkAfterImageUpdateForm(forms.ModelForm):
    class Meta:
        model = ReworkAfterImage
        fields = ('image',)

ReworkAfterFormset = inlineformset_factory(Rework, ReworkAfterImage,
    form = ReworkAfterImageUpdateForm,
    exclude = ('rework',),
    extra = 1,
    can_delete=True,
)

class ReworkNewForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class':'custom-file-input','multiple': True, }))
    class Meta:
        model=Rework
        fields='__all__'
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(pm=user)

#################################################################################################################################
#################################################################################################################################
class ProjectIssuesForm(forms.ModelForm):
    class Meta:
        model=ProjectIssues
        fields = '__all__'
        widgets={
            'date':forms.TextInput(attrs={'data-toggle':'datepicker'})
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(whm=user)

class ProjectIssuesNewForm(forms.ModelForm):
    class Meta:
        model=ProjectIssues
        fields = '__all__'

class SitePhotostForm(forms.ModelForm):
    class Meta:
        model=SitePhotos
        fields='__all__'
        widgets={
            'date':forms.TextInput(attrs={'data-toggle':'datepicker'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(whm=user)

class SitePhotostNewForm(forms.ModelForm):
    class Meta:
        model=SitePhotos
        fields='__all__'

class SitePhotostDetailsForm(forms.ModelForm):
    class Meta:
        model=SitePhotosDetails
        fields='__all__'
        exclude = ('reveal', 'sitephotos' )
        widgets={
            'image':forms.FileInput(attrs={'class':'custom-file-input','multiple': True, })
        }

SitePhotostFormset = inlineformset_factory(SitePhotos, SitePhotosDetails,
    form=SitePhotostNewForm,
    exclude=('project','date',),
    extra=0,
    can_delete=True,
    widgets={
        'reveal':forms.RadioSelect(),
    }  
)        

class PersonnelForm(forms.ModelForm):
    class Meta:
        model=Personnel
        fields='__all__'
        exclude = ('joborder_count',)

class SkillForm(forms.ModelForm):
    class Meta:
        model=PersonnelSkill
        fields='__all__'

class DailyReportForm(forms.ModelForm):
    class Meta:
        model=MaterialReport
        fields = '__all__'

DailyReportFormSet = inlineformset_factory(MaterialReport, MaterialReportDetails,
    form=DailyReportForm,
    extra=1,
    can_delete=True,
    widgets={
        'articles':forms.Select(attrs={'class':'form-control art', 'required':True}),
        'quantity':forms.NumberInput(attrs={'class':'form-control','required':True, 'min':0, "oninput":"validity.valid||(value='');"}),
        'remarks':forms.TextInput(attrs={'class':'form-control'}),
    }  
)

class InventoryAdminForm(forms.ModelForm):
    class Meta:
        model=ProjectInventory
        fields='__all__'

class WeeklyReportForm(forms.Form):
    report_type_choices=[
        ('requisition','Requisition'),
        ('externalorder','External order'),
        ('joborder','Joborder'),
        ('rework','Rework'),
        ('sitephotos','Site photos'),
        ('projectissues','Project issues'),
        ('materialreport','Material report'),
        ('externalmaterialreport','External material report'),
        ('projectinventory', 'Project inventory'),
        ('externalprojectinventory', 'External project inventory'),
    ]
    project = forms.ModelChoiceField(Project.objects.none(), label="Project Name")
    report = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=report_type_choices, label="Type of Report")
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user.groups.all()[0].name == "Admin":
            self.fields['project'].queryset = Project.objects.all()
        elif user.groups.all()[0].name == "Project Manager":
            self.fields['project'].queryset = Project.objects.filter(pm=user)
        elif user.groups.all()[0].name == "Person In-Charge":
            self.fields['project'].queryset = Project.objects.filter(pic=user)
           

class ExternalInventoryAdminForm(forms.ModelForm):
    class Meta:
        model = ExternalProjectInventory
        fields ='__all__'

class LandingPageTitleForm(forms.ModelForm):
    class Meta:
        model = LandingPageTitle
        fields='__all__'

class LandingPageImageForm(forms.ModelForm):
    class Meta:
        model=LandingPageImage
        fields='__all__'
        exclude = ('title',)
        widgets={
            'image':forms.FileInput(attrs={'class':'custom-file-input','multiple': True, })
        }

LandingPageImageFormset = inlineformset_factory(LandingPageTitle, LandingPageImage,
    form=LandingPageTitleForm,
    exclude=('title',),
    extra=1,
    can_delete=True,
)