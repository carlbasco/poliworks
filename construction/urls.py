from django.contrib.auth import views as auth_views
from django.conf.urls import *
from django.urls import path
from . import views
from .models import *

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),

    #Sign in/ Sign Out
    path('sign-in', views.signin, name="signin"),
    path('sign-out/', views.signout, name="signout"),

    #signuppages
    path('backoffice/signup/client', views.signupclient, name="signupclient"),
    path('backoffice/signup/whm', views.signupwhm, name="signupwhm"),
    path('backoffice/signup/pic', views.signuppic, name="signuppic"),
    path('backoffice/signup/pm', views.signuppm, name="signuppm"),

    #UserProfiles
    path('backoffice/profile', views.profile, name="userprofile"),
    path('backoffice/profile/edit', views.editprofile, name="editprofile"),
    path('backoffice/changepassword/', views.ChangePasswordView, name="change_password"),

    #newProject
    path('backoffice/createproject/', views.ProjectCreateView, name="project_create"),
    path('backoffice/project_list', views.ProjectListView, name="project_list"),
    path('backoffice/project/view/<int:pk>', views.ProjectDetailView, name="project_detail"),
    path('backoffice/project/view/<int:pk>/update', views.ProjectUpdateView, name="project_update"),

    #Quotation
    path('backoffice/project/create_quotation', views.QuotationCreateView.as_view(), name="quotation_create"),
    path('backoffice/project/quotation_list', views.QuotationListView, name="quotation_list"),
    path('backoffice/project/quotation/<int:pk>', views.QuotationDetailView, name="quotation_detail"),
    path('backoffice/project/quotation/<int:pk>/edit', views.QuotationUpdateView.as_view(), name="quotation_update"),
    path('backoffice/project/quotation/<int:pk>/delete', views.QuotationDeleteView, name="quotation_delete"),

    #ProjectProgress
    path('backoffice/project/progess/<int:pk>/edit', views.ProgressUpdateView, name="progress_update"),
    path('backoffice/project/progess/<int:pk>/delete', views.ProgressDeleteView, name="progress_delete"),

    #JobOrder
    path('backoffice/task/joborder', views.JobOrderCreateView.as_view(), name="joborder_create"),
    path('backoffice/task/joborder_list', views.JobOrderListView, name="joborder_list"),
    path('backoffice/task/joborder/<int:pk>', views.JobOrderDetailView, name="joborder_detail"),
    path('backoffice/task/joborder/<int:pk>/edit', views.JobOrderUpdateView.as_view(), name="joborder_update"),
    path('backoffice/task/joborder/<int:pk>/delete', views.JobOrderDeleteView, name="joborder_delete"),
    path('backoffice/task/joborder/<int:pk>/report', views.JobOrderReportView, name="joborder_report"),

    #Personnel
    path('backoffice/personnel/add', views.PersonnelCreateView, name="personnel_create"),
    path('backoffice/personnel/list',views.PersonnelListView, name="personnel_list"),
    path('backoffice/personnel/<int:pk>',views.PersonnelDetailView, name="personnel_detail"),
    path('backoffice/personnel/<int:pk>/edit',views.PersonnelUpdateView, name="personnel_update"),
    path('backoffice/personnel/<int:pk>/delete',views.PersonnelDeleteView, name="personnel_delete"),

    #Rework
    path('backoffice/task/rework', views.ReworkCreateView, name="rework_create"),
    path('backoffice/task/rework_list', views.ReworkListView, name="rework_list"),
    path('backoffice/task/rework/<int:pk>', views.ReworkDetailView, name="rework_detail"),
    path('backoffice/task/rework/<int:pk>/edit', views.ReworkUpdateView, name="rework_update"),
    path('backoffice/task/rework/<int:pk>/delete', views.ReworkDeleteView, name="rework_delete"),

    #Requisition
    path('backoffice/materials/create_requisition', views.RequisitionCreateView.as_view(), name="requisition_create"),
    path('backoffice/materials/requisition_list', views.RequisitionListView, name="requisition_list"),
    path('backoffice/materials/requisition/<int:pk>', views.RequisitionDetailView, name="requisition_detail"),
    path('backoffice/materials/requisition/<int:pk>/edit', views.RequisitionUpdateView.as_view(), name="requisition_update"),
    path('backoffice/materials/requisition/<int:pk>/delete', views.RequisitionDeleteView, name="requisition_delete"),
    
    #ExternalOrder
    path('backoffice/materials/create_externalorder', views.ExternalOrderCreateView.as_view(), name="externalorder_create"),
    path('backoffice/materials/externalorder_list', views.ExternalOrderListView, name="externalorder_list"),
    path('backoffice/materials/externalorder/<int:pk>', views.ExternalOrderDetailView, name="externalorder_detail"),
    path('backoffice/materials/externalorder/<int:pk>/edit', views.ExternalOrderUpdateView.as_view(), name="externalorder_update"),
    path('backoffice/materials/externalorder/<int:pk>/delete', views.ExternalOrderDeleteView, name="externalorder_delete"),

    #Reports
    path('backoffice/reports/daily', views.dailyreport, name="dailyreport"),
    path('backoffice/reports/issues', views.projectissues, name="issues"),

    #client
    path('myproject/', views.Client_home, name="client_home"),
    path('myproject/view/<int:pk>', views.ClientProjectView, name="client_view_project"),
    path('myproject/view/quotation/<int:pk>', views.ClientQuotationView, name="client_quotation"),
    path('profile', views.ClientProfileView, name="client_profile"),
    path('profile/edit', views.ClientProfileUpdateView, name="client_profile_update"),
    path('profile/changepassword', views.ClientChangePasswordView, name="client_change_password"),

    #account
    path('accounts/password/reset', auth_views.PasswordResetView.as_view(template_name="frontend/password_reset.html"),name="password_reset"),
    path('accounts/password/reset/sent', auth_views.PasswordResetDoneView.as_view(template_name="frontend/password_reset_done.html"),name="password_reset_done"),
    path('accounts/password/reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name="frontend/password_reset_confirm.html"), name="password_reset_confirm"),
    path('accounts/password/reset/complete', auth_views.PasswordResetCompleteView.as_view(template_name="frontend/password_reset_complete.html"), name="password_reset_complete"),


    #api get method
    path('backoffice/api/scope', views.ScopeOfWorks_api, name="ScopeOfWorks_api"),
    path('backoffice/api/scope/<int:pk>', views.ScopeOfWork_api, name="ScopeOfWork_api"),
    path('backoffice/api/materials/<int:pk>/', views.Inventory_api, name="Inventory_api"),
    path('backoffice/api/city/<int:pk>', views.City_api, name="Inventory_api"),
    
    #PM's page
    path('backoffice/pm/project_list', views.ProjectListView_PM, name="project_list_pm"),
    path('backoffice/pm/task/rework_list', views.ReworkListView_PM, name="rework_list_pm"),

    #PIC's page
    path('backoffice/pic/project_list', views.ProjectListView_PIC, name="project_list_pic"),
    path('backoffice/pic/joborder_list', views.JobOrderListView_PIC, name="joborder_list_pic"),

    #whm page
    path('backoffice/whm/joborder_list', views.JobOrderListView_WHM, name="joborder_list_whm"),

]
