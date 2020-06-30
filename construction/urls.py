from django.contrib.auth import views as auth_views
from django.conf.urls import *
from django.urls import path, re_path
from . import views
from .models import *


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),

    #Sign in/ Sign Out
    path('sign-in', views.signin, name="signin"),
    path('sign-out/', views.signout, name="signout"),

    #signuppages
    path('signup', views.SignupView, name="signup"),

    #UserProfiles
    path('profile', views.profile, name="userprofile"),
    path('profile/edit', views.editprofile, name="editprofile"),
    path('changepassword/', views.ChangePasswordView, name="change_password"),

    #newProject
    path('createproject/', views.ProjectCreateView, name="project_create"),
    path('project_list', views.ProjectListView, name="project_list"),
    path('project/view/<int:pk>', views.ProjectDetailView, name="project_detail"),
    path('project/view/<int:pk>/update', views.ProjectUpdateView, name="project_update"),

    #Quotation
    path('project/create_quotation', views.QuotationCreateView.as_view(), name="quotation_create"),
    path('project/quotation_list', views.QuotationListView, name="quotation_list"),
    path('project/quotation/<int:pk>', views.QuotationDetailView, name="quotation_detail"),
    path('project/quotation/<int:pk>/edit', views.QuotationUpdateView.as_view(), name="quotation_update"),
    path('project/quotation/<int:pk>/delete', views.QuotationDeleteView, name="quotation_delete"),

    #ProjectProgress
    path('project/progess/<int:pk>/edit', views.ProgressUpdateView, name="progress_update"),
    path('project/progess/<int:pk>/delete', views.ProgressDeleteView, name="progress_delete"),

    #JobOrder
    path('task/joborder', views.JobOrderCreateView.as_view(), name="joborder_create"),
    path('task/joborder_list', views.JobOrderListView, name="joborder_list"),
    path('task/joborder/<int:pk>', views.JobOrderDetailView, name="joborder_detail"),
    path('task/joborder/<int:pk>/edit', views.JobOrderUpdateView.as_view(), name="joborder_update"),
    path('task/joborder/<int:pk>/delete', views.JobOrderDeleteView, name="joborder_delete"),
    path('task/joborder/report/<int:pk>', views.JobOrderReportView, name="joborder_report"),

    #Personnel
    path('personnel/add', views.PersonnelCreateView, name="personnel_create"),
    path('personnel/list',views.PersonnelListView, name="personnel_list"),
    path('personnel/<int:pk>',views.PersonnelDetailView, name="personnel_detail"),
    path('personnel/<int:pk>/edit',views.PersonnelUpdateView, name="personnel_update"),
    path('personnel/<int:pk>/delete',views.PersonnelDeleteView, name="personnel_delete"),

    #Rework
    path('task/rework', views.ReworkCreateView.as_view(), name="rework_create"),
    path('task/rework_list', views.ReworkListView, name="rework_list"),
    path('task/rework/<int:pk>', views.ReworkDetailView, name="rework_detail"),
    path('task/rework/<int:pk>/edit', views.ReworkUpdateView.as_view(), name="rework_update"),
    path('task/rework/<int:pk>/delete', views.ReworkDeleteView, name="rework_delete"),

    #Requisition
    path('materials/create_requisition', views.RequisitionCreateView.as_view(), name="requisition_create"),
    path('materials/requisition_list', views.RequisitionListView, name="requisition_list"),
    path('materials/requisition/<int:pk>', views.RequisitionDetailView, name="requisition_detail"),
    path('materials/requisition/<int:pk>/edit', views.RequisitionUpdateView.as_view(), name="requisition_update"),
    path('materials/requisition/<int:pk>/delete', views.RequisitionDeleteView, name="requisition_delete"),
    path('materials/requisition/<int:pk>/action', views.RequisitionActionView, name="requisition_action"),
    
    #ExternalOrder
    path('materials/create_externalorder', views.ExternalOrderCreateView.as_view(), name="externalorder_create"),
    path('materials/externalorder_list', views.ExternalOrderListView, name="externalorder_list"),
    path('materials/externalorder/<int:pk>', views.ExternalOrderDetailView, name="externalorder_detail"),
    path('materials/externalorder/<int:pk>/edit', views.ExternalOrderUpdateView.as_view(), name="externalorder_update"),
    path('materials/externalorder/<int:pk>/delete', views.ExternalOrderDeleteView, name="externalorder_delete"),

    #Inventory
    path('materials/inventory_list', views.ProjectInventoryListView, name="inventory_list"),
    path('materials/inventory_list/external_inventory', views.ExternalProjectInventoryListView, name="external_inventory_list"),
    path('materials/inventory/<int:pk>', views.ProjectInventoryDetailView, name="inventory_detail"),
    path('materials/inventory/external/<int:pk>', views.ExternalProjectInventoryDetailView, name="external_inventory_detail"),

    #Reports
    path('reports/sitephotos', views.SitePhotosCreateView.as_view(), name="sitephotos"),
    path('reports/sitephotos_list', views.dailysitephotosListView, name="sitephotos_list"),
    path('reports/sitephotos/<int:pk>', views.dailysitephotosDetailView, name="sitephotos_detail"),
    path('reports/sitephotos/<int:pk>/update', views.dailysitephotosUpdateView, name="sitephotos_update"),
    path('reports/sitephotos/<int:pk>/delete', views.dailysitephotosDeleteView, name="sitephotos_delete"),
    path('reports/projectsite', views.ProjectReport.as_view(), name="projectreport"),
    path('reports/projectsite/results', views.ProjectReportPDF.as_view(), name="projectreportPDF"),

    # path('reports/issues', views.projectissues, name="issues"),
    path('reports/issues', views.ProjectIssuesCreateView.as_view(), name="issues"),
    path('reports/issues_list', views.ProjectIssuesList, name="issues_list"),
    path('reports/issues/<int:pk>', views.ProjectIssuesDetailView, name="issues_detail"),

    path('reports/materialreport_list', views. ProjectDailyReportListView, name="dailyreport_list"),

    path('reports/materialreport/<int:pk>', views. ProjectDailyReportDetailView, name="dailyreport_detail"),
    path('reports/materialreport/<int:pk>/delete', views. ProjectDailyReportDeleteView, name="materialreport_delete"),
    
    path('reports/materialreport/external/<int:pk>', views. ExternalOrderReportDetailView, name="external_report_detail"),
    path('reports/materialreport/external/<int:pk>/delete', views. ExternalOrderReportDeleteView, name="external_report_delete"),

    #client
    path('myproject/', views.Client_home, name="client_home"),
    path('myproject/view/<int:pk>', views.ClientProjectView, name="client_view_project"),
    path('myproject/sitephotos/view/<int:pk>', views.ClientSitePhotosView, name="client_sitephotos"),
    path('myproject/view/quotation/<int:pk>', views.ClientQuotationView, name="client_quotation"),
    path('myprofile', views.ClientProfileView, name="client_profile"),
    path('myprofile/edit', views.ClientProfileUpdateView, name="client_profile_update"),
    path('myprofile/changepassword', views.ClientChangePasswordView, name="client_change_password"),

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
    path('pm/project_list', views.ProjectListView_PM, name="project_list_pm"),
    path('pm/project/quotation_list', views.QuotationListView_PM, name="quotation_list_pm"),
    path('pm/inventory', views.ProjectInventoryList_PM, name="inventory_pm"),
    path('pm/inventory/external', views.ExternalProjectInventoryList_PM, name="external_inventory_pm"),
    path('pm/materials/requisition_list', views.RequisitionListView_PM, name="requisition_list_pm"),
    path('pm/materials/externalorder_list', views.ExternalOrderListView_PM, name="externalorder_list_pm"),
    path('pm/joborder_list', views.JobOrderListView_PM, name="joborder_list_pm"),
    path('pm/task/rework_list', views.ReworkListView_PM, name="rework_list_pm"),
    path('pm/reports/issues_list', views.ProjectIssuesList_PM, name="issues_list_pm"),
    path('pm/reports/dailyreport_list', views. ProjectDailyReportListView_PM, name="dailyreport_list_pm"),
    path('pm/reports/sitephotos_list', views.dailysitephotosListView_PM, name="sitephotos_list_pm"),

    #PIC's page
    path('pic/project_list', views.ProjectListView_PIC, name="project_list_pic"),
    path('pic/joborder_list', views.JobOrderListView_PIC, name="joborder_list_pic"),
    path('pic/task/rework_list', views.ReworkListView_PIC, name="rework_list_pic"),
    path('pic/reports/issues_list', views.ProjectIssuesList_PIC, name="issues_list_pic"),
    path('pic/inventory', views.ProjectInventoryList_PIC, name="inventory_pic"),
    path('pic/inventory/external', views.ExternalProjectInventoryList_PIC, name="external_inventory_pic"),
    path('pic/materials/requisition_list', views.RequisitionListView_PIC, name="requisition_list_pic"),
    path('pic/materials/externalorder_list', views.ExternalOrderListView_PIC, name="externalorder_list_pic"),
    path('pic/reports/dailyreport_list', views. ProjectDailyReportListView_PIC, name="dailyreport_list_pic"),
    path('pic/reports/sitephotos_list', views.dailysitephotosListView_PIC, name="sitephotos_list_pic"),

    #whm page
    path('whm/project_list', views.ProjectListView_WHM, name="project_list_whm"),
    path('whm/joborder_list', views.JobOrderListView_WHM, name="joborder_list_whm"),
    path('whm/requisition/<int:pk>/action', views.RequisitionActionView_WHM, name="requisition_action_whm"),
    path('whm/inventory', views.ProjectInventoryList_WHM, name="inventory_whm"),
    path('whm/inventory/external', views.ExternalProjectInventoryList_WHM, name="external_inventory_whm"),
    path('whm/inventory/<int:pk>', views.ProjectInventoryReport_WHM, name="inventory_whm_detail"),
    path('whm/inventory/external/<int:pk>', views.ExternalProjectInventoryReport_WHM, name="external_inventory_whm_detail"),
    path('whm/reports/issues_list', views.ProjectIssuesList_WHM, name="issues_list_whm"),
    path('whm/reports/issues/<int:pk>/edit', views.ProjectIssuesUpdateView.as_view(), name="issues_update"),
    path('reports/issues/<int:pk>/delete', views.ProjectIssuesDeleteView, name="issues_delete"),
    path('whm/materials/requisition_list', views.RequisitionListView_WHM, name="requisition_list_whm"),
    path('whm/materials/externalorder_list', views.ExternalOrderListView_WHM, name="externalorder_list_whm"),
    path('whm/reports/dailyreport_list', views. ProjectDailyReportListView_WHM, name="dailyreport_list_whm"),
    path('whm/reports/sitephotos_list', views.dailysitephotosListView_WHM, name="sitephotos_list_whm"),
    # path('whm/dailyreport', views.DailyReportCreateView, name="daily_report"),

]
