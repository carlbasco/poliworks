from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
from .forms import *
from .models import*


admin.site.site_header='Poliworks Inc'
admin.site.site_title='Poliworks Superuser'
admin.site.unregister(Group)
admin.site.site_url ='/sign-in'

class Profile(admin.TabularInline):
    model=Profile

@admin.register(User)    
class UserAdmin(ImportExportModelAdmin):
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
    
    def has_add_permission(self, request):
        return False

@admin.register(LandingPageCategory)
class LandingPageImageCategoryAdmin(admin.ModelAdmin):
    model = LandingPageCategory
    list_display=('name',)
    search_fields=('name',)

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
    search_fields =['name','id']
    ordering=('id','province')
    list_per_page=20

@admin.register(Project)
class projectdetails(ImportExportModelAdmin):
    exclude=('id',)
    list_display=('project','pm', 'client','typeofproject','startdate','status')

@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    model = Gender
    list_display = ('gender',)
    search_fields = ('gender',)
    ordering = ('gender',)

@admin.register(ProjectType)
class ProjectTypeAdmin(ImportExportModelAdmin):
    model = ProjectType
    list_display = ('projecttype',)    
    search_fields = ('projecttype',)    
    ordering = ('projecttype',)    

@admin.register(PersonnelType)
class PersonnelType(admin.ModelAdmin):
    model = PersonnelType
    list_display = ('personneltype', )
    search_fields = ('personneltype', )
    ordering = ('personneltype', )
############################################################################################
class QuotationDetailsAdmin(admin.TabularInline):
    model=QuotationDetails

class QuotationAdmin(admin.ModelAdmin):
    inlines = [QuotationDetailsAdmin]
    form = QuotationFormAdmin
    list_display = ('project','subject','date','amount','status' )
    search_fields = ('project', 'subject')
    ordering = ('date',)

admin.site.register(Quotation, QuotationAdmin)
############################################################################################
class RequisitionDeliveryAdmin(admin.TabularInline):
    model = RequisitionDelivery

class RequisitionAdmin(admin.ModelAdmin):
    inlines = [RequisitionDeliveryAdmin]
    form = RequisitionAdminForm
    list_display = ('project', 'date', 'whm', 'status')
    search_fields = ('project','date',)
    ordering = ('date',)

admin.site.register(Requisition, RequisitionAdmin)
############################################################################################
class JobOrderAdminTask(admin.TabularInline):
    model = JobOrderTask

class JobOrderAdmin(admin.ModelAdmin):
    inlines = [JobOrderAdminTask]
    form = JobOrderUpdateForm
    list_display = ('project', 'date',)
    search_fields = ('project', 'date',)
    ordering = ('date',)

admin.site.register(JobOrder, JobOrderAdmin)
############################################################################################
class ExternalOrderDetailsAdmin(admin.TabularInline):
    model = ExternalOrderDetails

class ExternalOrderAdmin(admin.ModelAdmin):
    inlines = [ExternalOrderDetailsAdmin]
    form = ExternalOrderUpdateForm
    list_display = ('project', 'date', 'whm')
    search_fields = ('project', 'date')
    ordering = ('date',)

admin.site.register(ExternalOrder, ExternalOrderAdmin)
############################################################################################
class spdetailsadmin(admin.TabularInline):
    model = SitePhotosDetails

class SitePhotosAdmin(admin.ModelAdmin):
    inlines = [spdetailsadmin]
    form = SitePhotostNewForm
    list_display = ('project', 'date',)
    search_fields = ('project', 'date',)
    ordering = ('date',)

admin.site.register(SitePhotos, SitePhotosAdmin)
############################################################################################
class dailyreport(admin.TabularInline):
    model = MaterialReportDetails

class DailyReportAdmin(admin.ModelAdmin):
    inlines = [dailyreport]
    form = DailyReportForm
    list_display = ('project', 'date',)
    search_fields = ('project', 'date',)
    ordering = ('date',)

admin.site.register(MaterialReport, DailyReportAdmin)
############################################################################################
class exdailyreport(admin.TabularInline):
    model = ExternalMaterialReportDetails

class ExternalMaterialReportAdmin(admin.ModelAdmin):
    inlines = [exdailyreport]
    form = ExternalMaterialReportForm
    list_display = ('project', 'date',)
    search_fields = ('project', 'date',)
    ordering = ('date',)

admin.site.register(ExternalMaterialReport, ExternalMaterialReportAdmin)
############################################################################################
@admin.register(ProjectIssues)
class ProjectIssueAdmin(admin.ModelAdmin):
    model = ProjectIssues
    form = ProjectIssuesNewForm
    list_display = ('project', 'date',)
    search_fields = ('project', 'date',)
    ordering = ('date',)
############################################################################################
@admin.register(Rework)
class ReworkAdmin(admin.ModelAdmin):
    model = Rework
    form = ReworkForm
    list_display = ('project', 'date', 'pm',)
    search_fields = ('project', 'date', 'pm',)
    ordering = ('date',)
############################################################################################

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
class PersonnelAdmin(ImportExportModelAdmin):
    list_display = ('short_name','personnel_type')

@admin.register(Inventory)
class Inventory(ImportExportModelAdmin):
    list_display = ('description','alternate_code','item_code','quantity', 'unit_price')
    search_fields = ('description','alternate_code','item_code','quantity')
    list_per_page = 20
    ordering = ('pk',)


class ExternalInventoryDetailsAdmin(admin.TabularInline):
    model = ExternalProjectInventoryDetails

class ExternalInventoryAdmin(admin.ModelAdmin):
    inlines = [ExternalInventoryDetailsAdmin]
    form = ExternalInventoryAdminForm
    list_display = ('project',)
    search_fields = ('project', )

admin.site.register(ExternalProjectInventory, ExternalInventoryAdmin)

class InventoryDetailsAdmin(admin.TabularInline):
    model = ProjectInventoryDetails

class ProjectInventoryAdmin(admin.ModelAdmin):
    inlines = [InventoryDetailsAdmin]
    form = InventoryAdminForm
    list_display = ('project', 'last_update')
    search_fields= ('project',)
    

admin.site.register(ProjectInventory, ProjectInventoryAdmin)

