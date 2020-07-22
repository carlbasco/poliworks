from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *


@receiver(post_save, sender=Estimate)
def EstimateNotif(sender, instance, created, **kwargs):
    if created:
        admin = User.objects.filter(groups__name="Admin")
        for i in admin:
            adnin_notif = Notification.objects.create(receiver=i, description=f"{instance.name} has sent an Estimate", url=f"/project/estimate/{instance.id}")


@receiver(post_save, sender=Inquiry)
def InquiryNotif(sender, instance, created, **kwargs):
    if created:
        admin = User.objects.filter(groups__name="Admin")
        for i in admin:
            adnin_notif = Notification.objects.create(receiver=i, description=f"{instance.name} has sent an Inquiry", url=f"/project/inquiry/{instance.id}")
            

@receiver(post_save, sender=Project)
def ProjectNotif(sender, instance, created, **kwargs):
    if created:
        admin = User.objects.filter(groups__name="Admin")
        for i in admin:
            adnin_notif = Notification.objects.create(receiver=i, description=f"New Project has been created", url=f"/project/view/{instance.id}")
        client_notif = Notification.objects.create(receiver=instance.client, description=f"New Project has been created", url=f"/myproject/view/{instance.id}")
        pm_notif = Notification.objects.create(receiver=instance.pm, description=f"New Project has been created", url=f"/project/view/{instance.id}")

@receiver(post_save, sender=Quotation)
def QuotationNotif(sender, instance, created, **kwargs):
    if created:
        admin = User.objects.filter(groups__name="Admin")
        for i in admin:
            admin_notif = Notification.objects.create(receiver=i, description=f"Quotation at {instance.project} has been created ", url=f"/project/quotation/{instance.id}")
            admin_notif.save()
        client_notif = Notification.objects.create(receiver=instance.project.client, description=f"Quotation at {instance.project} has been created ", url=f"/myproject/view/quotation/{instance.id}")
        
@receiver(post_save, sender=ProjectProgress)
def ProgressNotif(sender, instance, created, **kwargs):
    if created == False:
        data = Project.objects.get(project=instance.project)
        if instance.total_progress == 100:
            if data.comdate < datetime.date.today():
                data.status = "Completed (Overdue)"
                data.save()
            else:
                data.status = "Completed"
                data.save()
        else:
            data.status = "On-going"
            data.save() 
        admin = User.objects.filter(groups__name="Admin")
        for i in admin:
            adnin_notif = Notification.objects.create(receiver=i, description=f"Progress in project {data.project} has been updated", url=f"/project/view/{data.id}")
        client_notif = Notification.objects.create(receiver=data.client, description=f"Progress in project {data.project} has been updated", url=f"/myproject/view/{data.id}")
        pm_notif = Notification.objects.create(receiver=data.pm, description=f"Progress in project {data.project} has been updated", url=f"/project/view/{data.id}")
        pic_notif = Notification.objects.create(receiver=data.pic, description=f"Progress in project {data.project} has been updated", url=f"/project/view/{data.id}")
        print("Progress Update")

@receiver(post_save, sender=Requisition)
def RequisitionNotif(sender, instance, created, **kwargs):
    if created:
        admin = User.objects.filter(groups__name="Admin")
        for i in admin:
            adnin_notif = Notification.objects.create(receiver=i, description=f"{instance.whm} has sent a requisition on  Project {instance.project}", url=f"/materials/requisition/{instance.id}")
        pm_notif = Notification.objects.create(receiver=instance.project.pm, description=f"{instance.whm} has sent a requisition on  Project {instance.project}", url=f"/materials/requisition/{instance.id}")
        pic_notif = Notification.objects.create(receiver=instance.project.pic, description=f"{instance.whm} has sent a requisition on  Project {instance.project}", url=f"/materials/requisition/{instance.id}")


@receiver(post_save, sender=ExternalOrder)
def ExternalOrderNotif(sender, instance, created, **kwargs):
    if created:
        admin = User.objects.filter(groups__name="Admin")
        for i in admin:
            adnin_notif = Notification.objects.create(receiver=i, description=f"External Order has been created at project {instance.project}", url=f"/materials/externalorder/{instance.id}")
        pm_notif = Notification.objects.create(receiver=instance.project.pm, description=f"External Order has been created at project {instance.project}", url=f"/materials/externalorder/{instance.id}")
        pic_notif = Notification.objects.create(receiver=instance.project.pic, description=f"External Order has been created at project {instance.project}", url=f"/materials/externalorder/{instance.id}")
    
@receiver(post_save, sender=JobOrder)
def JobOrderNotif(sender, instance, created, **kwargs):
    if created:
        admin = User.objects.filter(groups__name="Admin")
        for i in admin:
            adnin_notif = Notification.objects.create(receiver=i, description=f"Job Order at project {instance.project} has been created", url=f"/task/joborder/{instance.id}")
        pm_notif = Notification.objects.create(receiver=instance.project.pm, description=f"Job Order at project {instance.project} has been created", url=f"/task/joborder/{instance.id}")
        whm_notif = Notification.objects.create(receiver=instance.project.whm, description=f"Job Order at project {instance.project} has been created", url=f"/task/joborder/{instance.id}")

        
@receiver(post_save, sender=Personnel)
def PersonnelNotif(sender, instance, created, **kwargs):
    if created:
        admin = User.objects.filter(groups__name="Admin")
        for i in admin:
            adnin_notif = Notification.objects.create(receiver=i, description=f"New Personnel has been added", url=f"/personnel/{instance.id}")
    # else:
    #     admin = User.objects.filter(groups__name="Admin")
    #     for i in admin:
    #         adnin_notif = Notification.objects.create(receiver=i, description=f"{instance.short_name()} 's information has been updated'", url=f"/personnel/{instance.id}")
@receiver(post_save, sender=Rework)
def ReworkNotif(sender, instance, created, **kwargs):
    if created:
        admin = User.objects.filter(groups__name="Admin")
        for i in admin:
            adnin_notif = Notification.objects.create(receiver=i, description=f"Rework at project {instance.project} has been created", url=f"/task/rework/{instance.id}")
        pic_notif = Notification.objects.create(receiver=instance.project.pic, description=f"Rework at project {instance.project} has been created", url=f"/task/rework/{instance.id}")
    else:
        admin = User.objects.filter(groups__name="Admin")
        for i in admin:
            adnin_notif = Notification.objects.create(receiver=i, description=f"Rework at project {instance.project} has been updated", url=f"/task/rework/{instance.id}")
        pic_notif = Notification.objects.create(receiver=instance.project.pic, description=f"Rework at project {instance.project} has been updated", url=f"/task/rework/{instance.id}")

@receiver(post_save, sender=ProjectIssues)
def ProjectIssueNotif(sender, instance, created, **kwargs):
    if created:
        admin = User.objects.filter(groups__name="Admin")
        for i in admin:
            adnin_notif = Notification.objects.create(receiver=i, description=f"Project Issue at project {instance.project} has been created", url=f"/reports/issues/{instance.id}")
        pm_notif = Notification.objects.create(receiver=instance.project.pm, description=f"Project Issue at project {instance.project} has been created", url=f"/reports/issues/{instance.id}")
        pic_notif = Notification.objects.create(receiver=instance.project.pic, description=f"Project Issue at project {instance.project} has been created", url=f"/reports/issues/{instance.id}")
    else:
        admin = User.objects.filter(groups__name="Admin")
        for i in admin:
            adnin_notif = Notification.objects.create(receiver=i, description=f"Project Issue at project {instance.project} has been updated", url=f"/reports/issues/{instance.id}")
        pm_notif = Notification.objects.create(receiver=instance.project.pm, description=f"Project Issue at project {instance.project} has been updated", url=f"/reports/issues/{instance.id}")
        pic_notif = Notification.objects.create(receiver=instance.project.pic, description=f"Project Issue at project {instance.project} has been updated", url=f"/reports/issues/{instance.id}")

@receiver(post_save, sender=SitePhotos)
def SitePhotosNotif(sender, instance, created, **kwargs):
    if created:
        admin = User.objects.filter(groups__name="Admin")
        for i in admin:
            adnin_notif = Notification.objects.create(receiver=i, description=f"New Site Photos at project {instance.project} has been created", url=f"/reports/sitephotos/{instance.id}")            
        pm_notif = Notification.objects.create(receiver=instance.project.pm, description=f"New Site Photos at project {instance.project} has been created", url=f"/reports/sitephotos/{instance.id}")
        pic_notif = Notification.objects.create(receiver=instance.project.pic, description=f"New Site Photos at project {instance.project} has been created", url=f"/reports/sitephotos/{instance.id}")

@receiver(post_save, sender=LandingPageTitle)
def LandingPageNotif(sender, instance, created, **kwargs):
    admin = User.objects.filter(groups__name="Admin")
    for i in admin:
        adnin_notif = Notification.objects.create(receiver=i, description=f"New Images for Landing Page has been created", url=f"/admin/landingpage/{instance.id}")
