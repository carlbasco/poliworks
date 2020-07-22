# Generated by Django 3.0.8 on 2020-07-22 03:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0020_auto_20200722_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobordertask',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Done', 'Done'), ('On-going', 'On-going')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='personneljoborder',
            name='joborder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='construction.JobOrderTask'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Completed (Overdue)', 'Completed (Overdue)'), ('Completed', 'Completed'), ('On-going', 'On-going')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='level',
            field=models.IntegerField(choices=[(5, 'high'), (3, 'medium'), (1, 'low')], default=1, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Done', 'Done'), ('On-going', 'On-going')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Rejected', 'Rejected'), ('Accepted', 'Accepted')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='status',
            field=models.CharField(choices=[('Closed', 'Closed'), ('Pending', 'Pending'), ('To be Delivered', 'To be Delivered')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='requisitiondelivery',
            name='status2',
            field=models.CharField(blank=True, choices=[('Not Received', 'Not Received'), ('Incomplete', 'Incomplete'), ('Complete', 'Complete')], max_length=255, null=True, verbose_name='Action'),
        ),
    ]
