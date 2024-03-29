# Generated by Django 3.0.8 on 2020-10-22 05:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0002_auto_20200729_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobordertask',
            name='status',
            field=models.CharField(choices=[('On-going', 'On-going'), ('Pending', 'Pending'), ('Done', 'Done')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='project',
            name='client',
            field=models.ForeignKey(limit_choices_to={'groups__name': 'Client'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_client', to=settings.AUTH_USER_MODEL, verbose_name='Client'),
        ),
        migrations.AlterField(
            model_name='project',
            name='pm',
            field=models.ForeignKey(limit_choices_to={'groups__name': 'Project Manager'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_pm', to=settings.AUTH_USER_MODEL, verbose_name='Project Manager'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(blank=True, choices=[('On-going', 'On-going'), ('Pending', 'Pending'), ('Completed', 'Completed'), ('Completed (Overdue)', 'Completed (Overdue)')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='level',
            field=models.IntegerField(choices=[(5, 'high'), (1, 'low'), (3, 'medium')], default=1, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='status',
            field=models.CharField(choices=[('On-going', 'On-going'), ('Pending', 'Pending'), ('Done', 'Done')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='requisitiondelivery',
            name='status2',
            field=models.CharField(blank=True, choices=[('Incomplete', 'Incomplete'), ('Not Received', 'Not Received'), ('Complete', 'Complete')], max_length=255, null=True, verbose_name='Action'),
        ),
    ]
