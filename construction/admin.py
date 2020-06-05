from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
from .forms import *
from .models import*


admin.site.site_header='Poliworks Inc'
admin.site.site_title='Poliworks Superuser'
# admin.site.unregister(Group)

class Profile(admin.TabularInline):
    model=Profile
    
class UserAdmin(BaseUserAdmin):
    inlines=[Profile]
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ('email','full_name')
    list_filter = ('groups',)
    fieldsets = (
        (None, 
        {'fields': ('email', 'password','first_name','middle_name','last_name','suffix')}),
        ('Role', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','first_name','middle_name','last_name','suffix', 'groups')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)

@admin.register(Province)
class ProvinceAdmin(ImportExportModelAdmin):
    list_display=('id','name',)
    search_fields =('name','id')
    ordering=('id',)
    list_per_page=20

@admin.register(City)
class CityAdmin(ImportExportModelAdmin):
    exclude = ('id', )
    list_display=('id','name','province')
    search_fields =('name','province')
    ordering=('id','province')
    list_per_page=20

@admin.register(ProjectSite)
class projectdetails(ImportExportModelAdmin):
    exclude=('id',)
    list_display=(
        'pm', 'client','projectsite','typeofproject','startdate','status'
    )

@admin.register(PersonnelSkill)
class personnel_skill(ImportExportModelAdmin):
    exclude=('id', )

@admin.register(ScopeOfWorkCategory)
class ScopeOfWorkCategory(ImportExportModelAdmin):
    list_display=('category',)
    ordering=('pk',)

@admin.register(ScopeOfWork)
class ScopeOfWork(ImportExportModelAdmin):
    list_display=('scope', 'category','materialcost','laborcost','subbid','get_cost')
    search_fields=('scope',)
    list_per_page=20
    list_filter=('category',)
    ordering=('pk',)


@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('full_name','skill','personnel_type')

@admin.register(Inventory)
class Inventory(ImportExportModelAdmin):
    list_display = ('alternate_code','item_code','description','quantity', 'unit_price')
    search_fields = ('alternate_code','item_code','description',)
    list_per_page = 20
    ordering = ('pk',)

class QuotationDetailsAdmin(admin.TabularInline):
    model=QuotationDetails
class QuotationAdmin(admin.ModelAdmin):
    inlines = [QuotationDetailsAdmin]
    form = QuotationFormAdmin
    list_display = ('projectsite','subject','date','amount','status' )
    search_fields = ('projectsite', 'subject')
    ordering = ('date',)

admin.site.register(Quotation, QuotationAdmin)