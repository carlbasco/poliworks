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
        
class SignupFormWHM(forms.ModelForm):
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
        user = super(SignupFormWHM, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            group = Group.objects.get(name='Warehouseman') 
            group.user_set.add(user)
        return user

class SignupFormPIC(forms.ModelForm):
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
        user = super(SignupFormPIC, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            group = Group.objects.get(name='Person In-Charge') 
            group.user_set.add(user)
        return user

class SignupFormPM(forms.ModelForm):
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
        user = super(SignupFormPM, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            group = Group.objects.get(name='Project Manager') 
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
    tcost = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control tcost','readonly':'true'}))
    class Meta:
        model=Quotation
        fields='__all__'

class QuotationFormAdmin(forms.ModelForm):
    class Meta:
        model=Quotation
        fields='__all__'
        
QuotationFormSet = inlineformset_factory(Quotation, QuotationDetails,
    form=QuotationForm,
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

QuotationUpdateFormSet = inlineformset_factory(
    Quotation, QuotationDetails,
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
        exclude=('total_progress',)

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
    unit = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control unit','readonly':'true'}))
    class Meta:
        model=Requisition
        fields='__all__'

class RequisitionActionForm(forms.ModelForm):
    class Meta:
        model=Requisition
        fields='__all__'
        

RequisitionFormSet = inlineformset_factory(
    Requisition, RequisitionDetails, 
    form=RequisitionForm, 
    extra=1,
    can_delete=True,
    exclude=('status',),
    widgets={
        'quantity':forms.NumberInput(attrs={'class':'form-control'}),
        'articles':forms.Select(attrs={'class':'form-control art'})
    }
)

RequisitionUpdateFormSet = inlineformset_factory(
    Requisition, RequisitionDetails, 
    form=RequisitionForm, 
    extra=0,
    can_delete=True,
    exclude=('status',),
    widgets={
        'quantity':forms.NumberInput(attrs={'class':'form-control', 'required':'true'}),
        'articles':forms.Select(attrs={'class':'form-control art'})
    }
)

RequisitionActionFormSet = inlineformset_factory(
    Requisition, RequisitionDetails, 
    form=RequisitionActionForm, 
    exclude=('requisition','quantity','articles',),
    extra=0,
    widgets={
        'status':forms.Select(attrs={'class':'form-control', }),
    }
)
#################################################################################################################################
#################################################################################################################################
class ExternalOrderForm(forms.ModelForm):
    totalprice = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control total_price','readonly':'true'}), required=False)
    class Meta:
        model = ExternalOrder
        fields='__all__'

class ExternalOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = ExternalOrder
        fields='__all__'

ExternalOrderFormSet = inlineformset_factory(
    ExternalOrder, ExternalOrderDetails,
    form=ExternalOrderForm,
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

#################################################################################################################################
#################################################################################################################################
class JobOrderForm(forms.ModelForm):
    personnel = forms.ModelChoiceField(queryset=Personnel.objects.filter(status="Available"), widget=forms.Select(attrs={'class':'form-control personnel', 'required': 'true'}))
    class Meta:
        model=JobOrder
        fields='__all__'

class JobOrderUpdateForm(forms.ModelForm):
    class Meta:
        model=JobOrder
        fields='__all__'

class JobOrderTasksForm(forms.ModelForm):
    class Meta:
        model=JobOrderTask
        fields='__all__'

JobOrderFormSet = inlineformset_factory(
    JobOrder, JobOrderTask,
    form=JobOrderForm,
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

JobOrderUpdateFormSet = inlineformset_factory(
    JobOrder, JobOrderTask,
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

JobOrderReportFormSet = inlineformset_factory(
    JobOrder, JobOrderTask,
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

#################################################################################################################################
#################################################################################################################################
class WeeklyStatusReportForm(forms.ModelForm):
    class Meta:
        model=WeeklyStatusReport
        fields='__all__'

class ProjectStatusForm(forms.ModelForm):
    class Meta:
        model=ProjectStatus
        fields='__all__'

class SitePhotosFrom(forms.ModelForm):
    class Meta:
        model=SitePhotos
        fields='__all__'
    
class ManpowerForm(forms.ModelForm):
    class Meta:
        model=Manpower
        fields='__all__'

class ProjectSolutionForm(forms.ModelForm):
    class Meta:
        model=ProjectSolution
        fields='__all__'

class RequestForTheWeekForm(forms.ModelForm):
    class Meta:
        model=RequestForTheWeek
        fields='__all__'

class ProblemForm(forms.ModelForm):
    class Meta:
        model=ProjectIssues
        fields='__all__'

class DailyReportForm(forms.ModelForm):
    class Meta:
        model=DailyReport
        fields='__all__'
        widgets={
            'image':forms.ClearableFileInput(attrs={'multiple': True})
        }

class PersonnelForm(forms.ModelForm):
    class Meta:
        model=Personnel
        fields='__all__'
        exclude = ('status','projectsite')

class SkillForm(forms.ModelForm):
    class Meta:
        model=PersonnelSkill
        fields='__all__'
