# Generated by Django 3.0.7 on 2020-06-10 21:31

import construction.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0034_auto_20200611_0509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobordertask',
            name='status',
            field=models.CharField(choices=[('Done', 'Done'), ('Pending', 'Pending'), ('On-going', 'On-going')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='sex',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, verbose_name='Sex'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('Currently Assigned', 'Currently Assigned')], default='Available', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='level',
            field=models.IntegerField(choices=[(1, 'low'), (3, 'medium'), (5, 'high')], default=1, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='status',
            field=models.CharField(choices=[('Done', 'Done'), ('Pending', 'Pending'), ('On-going', 'On-going')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('On-going', 'On-going'), ('Completed', 'Completed')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='typeofproject',
            field=models.CharField(choices=[('General Construction', 'General Construction'), ('Interior Fit-out Works', 'Interior Fit-outWorks'), ('Concrete Countertops', 'Concrete Countertops'), ('Industrial Cement Flooring Finish', 'Industrial Cement Flooring Finish'), ('Self-Leveling Floor Applcation', 'Self-Leveling Floor Applcation')], max_length=255, null=True, verbose_name='Project Type'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('Rejected', 'Rejected'), ('Pending', 'Pending'), ('Accepted', 'Accepted')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='status',
            field=models.CharField(choices=[('Closed', 'Closed'), ('Pending', 'Pending'), ('To be Delivered', 'To be Delivered')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='sitephotosdetails',
            name='image',
            field=models.FileField(upload_to=construction.models.project_sitephotos_path, verbose_name='Photos'),
        ),
    ]
