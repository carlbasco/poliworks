from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms.models import inlineformset_factory
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
    choice = {('Project Manager', 'Project Manager'), ('Person In-Charge', 'Person In-Charge'), ('Warehouseman', 'Warehouseman'), ('Client', 'Client')}
    account = forms.ChoiceField(label="Account Type", choices=choice)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    cpassword = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email','first_name','middle_name','last_name','suffix']

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

class SignupFormClient(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    cpassword = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email','first_name','middle_name','last_name','suffix']

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
        user = super(SignupFormClient, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            group = Group.objects.get(name='Client') 
            group.user_set.add(user)
        return user
        
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
        model = ProjectSite
        fields = '__all__'
        exclude = ('whm', 'pic')
        widgets={
            'design' : forms.FileInput(attrs={'class':'custom-file-input'})
        }

class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = ProjectSite
        fields = '__all__'
        exclude = ('pm', 'client')
        widgets={
            'design' : forms.FileInput(attrs={'class':'custom-file-input'})
        }

class ProjectUpdateStaffForm(forms.ModelForm):
    class Meta:
        model = ProjectSite
        fields = ('whm', 'pic')
        
class ProjectViewForm(forms.ModelForm):
    class Meta:
        model=ProjectSite
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
        self.fields['projectsite'].queryset = ProjectSite.objects.filter(pm=user)

class QuotationNewForm(forms.ModelForm):
    tcost = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control tcost','readonly':'true'}))
    class Meta:
        model=Quotation
        fields='__all__'

class QuotationFormAdmin(forms.ModelForm):
    class Meta:
        model=Quotation
        fields='__all__'
        
QuotationFormSet = inlineformset_factory(Quotation, QuotationDetails,
    form=QuotationNewForm,
    extra=1,
    can_delete=True,
    widgets={
        'scope_of_work':forms.Select(attrs={'class':'sow', }),
        'unit':forms.TextInput(attrs={'class':'form-control',}),
        'quantity':forms.NumberInput( attrs={'class':'form-control qty','required': 'true'}),
    }
)

class QuotationUpdateForm(forms.ModelForm):
    class Meta:
        model=Quotation
        fields='__all__'

QuotationUpdateFormSet = inlineformset_factory(Quotation, QuotationDetails,
    form=QuotationUpdateForm,
    extra=0,
    can_delete=True,
    widgets={
        'scope_of_work':forms.Select(attrs={'class':'sow', }),
        'unit':forms.TextInput(attrs={'class':'form-control',}),
        'quantity':forms.NumberInput( attrs={'class':'form-control qty','required': 'true'}),
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
        exclude = ('status',)
        

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RequisitionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['projectsite'].queryset = ProjectSite.objects.filter(whm=user)

class RequisitionNewForm(forms.ModelForm):
    unit = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control unit','readonly':'true', 'required':'false'}))
    class Meta:
        model = Requisition
        fields ='__all__'

RequisitionFormSet = inlineformset_factory(Requisition, RequisitionDetails, 
    form = RequisitionNewForm, 
    extra = 1,
    can_delete = True,
    exclude = ('status', 'status2', 'quantity2'),
    widgets={
        'quantity':forms.NumberInput(attrs={'class':'form-control'}),
        'articles':forms.Select(attrs={'class':'form-control art'})
    }
)

RequisitionUpdateFormSet = inlineformset_factory(Requisition, RequisitionDetails, 
    form=RequisitionNewForm, 
    extra=0,
    can_delete=True,
    exclude = ('status', 'status2', 'quantity2'),
    widgets={
        'quantity':forms.NumberInput(attrs={'class':'form-control', 'required':'true'}),
        'articles':forms.Select(attrs={'class':'form-control art'})
    }
)

class RequisitionActionForm(forms.ModelForm):
    class Meta:
        model=Requisition
        fields='__all__'
        
RequisitionActionFormSet = inlineformset_factory(Requisition, RequisitionDetails, 
    form=RequisitionActionForm, 
    exclude=('requisition','quantity','articles','quantity2'),
    extra=0,
    widgets={'status':forms.Select(attrs={'class':'form-control', 'required':True})}
)

RequisitionActionFormSet_whm = inlineformset_factory(Requisition, RequisitionDetails, 
    form=RequisitionActionForm, 
    exclude=('requisition','quantity','articles','status'),
    extra=0,
    widgets={
        'status2':forms.Select(attrs={'class':'form-control', 'required':True}),
        'quantity2':forms.NumberInput(attrs={'class':'form-control','placeholder':'leave it blank if complete or not recieved'}),
    }
)
#################################################################################################################################
#################################################################################################################################
class ExternalOrderForm(forms.ModelForm):
    class Meta:
        model = ExternalOrder
        fields = '__all__'
        exclude = ('amount',)
        widgets={
            'image' : forms.FileInput(attrs={'class':'custom-file-input'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['projectsite'].queryset = ProjectSite.objects.filter(whm=user)

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
        'unit':forms.TextInput(attrs={'class':'form-control'}),
        'articles':forms.TextInput(attrs={'class':'form-control','required': 'true'}),
        'unitprice':forms.NumberInput(attrs={'class':'form-control','required': 'true'})
    }    
)

ExternalOrderUpdateFormSet = inlineformset_factory(ExternalOrder, ExternalOrderDetails,
    form=ExternalOrderUpdateForm,
    extra=0,
    can_delete=True,
    widgets={
        'quantity':forms.NumberInput(attrs={'class':'form-control','required': 'true'}),
        'unit':forms.TextInput(attrs={'class':'form-control','required': 'true'}),
        'articles':forms.TextInput(attrs={'class':'form-control','required': 'true'}),
        'unitprice':forms.NumberInput(attrs={'class':'form-control','required': 'true'})
    }    
)
class ExternalOrderReportForm(forms.ModelForm):
    class Meta:
        model = ExternalOrderReport
        fields = '__all__'

ExternalOrderReportFormSet = inlineformset_factory(ExternalOrderReport, ExternalOrderDetailsReport,
    form=ExternalOrderReportForm,
    extra=1,
    can_delete=True,
    widgets={
        'articles':forms.Select(attrs={'class':'form-control art'}),
        'quantity':forms.NumberInput(attrs={'class':'form-control','required': 'true'}),
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
        self.fields['projectsite'].queryset = ProjectSite.objects.filter(pic=user)

class JobOrderNewForm(forms.ModelForm):
    personnel = forms.ModelChoiceField(queryset=Personnel.objects.filter(status="Available"), widget=forms.Select(attrs={'class':'form-control personnel', 'required': 'true'}))
    class Meta:
        model=JobOrder
        fields='__all__'

JobOrderFormSet = inlineformset_factory(JobOrder, JobOrderTask,
    form=JobOrderNewForm,
    exclude=('completion_date', 'status',),
    extra=1,
    can_delete=True,
    widgets={
        'activity':forms.TextInput( attrs={'class':'form-control'}),
        'date':forms.DateInput( attrs={'class':'form-control dateinput'}),
        'date2':forms.DateInput( attrs={'class':'form-control dateinput'}),
        'remarks':forms.TextInput( attrs={'class':'form-control'}),
    }  
)

class JobOrderUpdateForm(forms.ModelForm):
    class Meta:
        model=JobOrder
        fields='__all__'

JobOrderUpdateFormSet = inlineformset_factory(JobOrder, JobOrderTask,
    form=JobOrderUpdateForm,
    exclude=('completion_date', 'status',),
    extra=0,
    can_delete=True,
    widgets={
        'personnel':forms.Select(attrs={'class':'form-control personnel'}),
        'activity':forms.TextInput( attrs={'class':'form-control'}),
        'date':forms.DateInput( attrs={'class':'form-control dateinput'}),
        'date2':forms.DateInput( attrs={'class':'form-control dateinput'}),
        'remarks':forms.TextInput( attrs={'class':'form-control'}),
    }  
)

class JobOrderTasksForm(forms.ModelForm):
    class Meta:
        model=JobOrderTask
        fields='__all__'

JobOrderReportFormSet = inlineformset_factory(JobOrder, JobOrderTask,
    form=JobOrderUpdateForm,
    exclude=('activity', 'date','date2','personnel','completion_date', 'remarks'),
    extra=0,
    can_delete=False,
    widgets={
        'remarks':forms.TextInput(attrs={'class':'form-control'}),
        'status':forms.Select(attrs={'class':'form-control'}),
    }  
)

#################################################################################################################################
#################################################################################################################################
class ReworkForm(forms.ModelForm):
    class Meta:
        model=Rework
        fields='__all__'
        

class ReworkNewForm(forms.ModelForm):
    class Meta:
        model=Rework
        fields='__all__'
        widgets={
            'date':forms.TextInput(attrs={'data-toggle':'datepicker'})
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['projectsite'].queryset = ProjectSite.objects.filter(pm=user)

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
        self.fields['projectsite'].queryset = ProjectSite.objects.filter(whm=user)

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
        self.fields['projectsite'].queryset = ProjectSite.objects.filter(whm=user)

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
    exclude=('projectsite','date',),
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
        exclude = ('status','projectsite')

class SkillForm(forms.ModelForm):
    class Meta:
        model=PersonnelSkill
        fields='__all__'

class DailyReportForm(forms.ModelForm):
    class Meta:
        model=ProjectDailyReport
        fields = '__all__'

DailyReportFormSet = inlineformset_factory(ProjectDailyReport, ProjectDailyReportDetails,
    form=DailyReportForm,
    extra=1,
    can_delete=True,
    widgets={
        'articles':forms.Select(attrs={'class':'form-control art'}),
        'quantity':forms.NumberInput(attrs={'class':'form-control'}),
        'remarks':forms.TextInput(attrs={'class':'form-control'}),
    }  
)

class InventoryAdminForm(forms.ModelForm):
    class Meta:
        model=ProjectInventory
        fields='__all__'

class WeeklyReportForm(forms.Form):
    projectsite = forms.ModelChoiceField(ProjectSite.objects.none(), label="Project Site")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user.groups.all()[0].name == "Admin":
            self.fields['projectsite'].queryset = ProjectSite.objects.all()
        elif user.groups.all()[0].name == "Project Manager":
            self.fields['projectsite'].queryset = ProjectSite.objects.filter(pm=user)
        elif user.groups.all()[0].name == "Person In-Charge":
            self.fields['projectsite'].queryset = ProjectSite.objects.filter(pic=user)
           

class ExternalInventoryAdminForm(forms.ModelForm):
    class Meta:
        model = ExternalProjectInventory
        fields ='__all__'