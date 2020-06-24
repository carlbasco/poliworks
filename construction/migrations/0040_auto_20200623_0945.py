# Generated by Django 3.0.7 on 2020-06-23 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0039_auto_20200622_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='externalorder',
            name='or_image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='OR Image'),
        ),
        migrations.AddField(
            model_name='projectprogressdetails',
            name='completion_date',
            field=models.DateField(blank=True, null=True, verbose_name='Completion Date'),
        ),
        migrations.AlterField(
            model_name='jobordertask',
            name='status',
            field=models.CharField(choices=[('On-going', 'On-going'), ('Done', 'Done'), ('Pending', 'Pending')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='personnel_type',
            field=models.CharField(choices=[('Company Worker', 'Company Worker'), ('Subcontractor', 'Subcontractor')], max_length=255, verbose_name='Type of Personnel'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='sex',
            field=models.CharField(choices=[('Female', 'Female'), ('Male', 'Male')], max_length=10, verbose_name='Sex'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='status',
            field=models.CharField(choices=[('Currently Assigned', 'Currently Assigned'), ('Available', 'Available')], default='Available', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='level',
            field=models.IntegerField(choices=[(5, 'high'), (3, 'medium'), (1, 'low')], default=1, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='status',
            field=models.CharField(choices=[('On-going', 'On-going'), ('Done', 'Done'), ('Pending', 'Pending')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='status',
            field=models.CharField(blank=True, choices=[('On-going', 'On-going'), ('Completed', 'Completed'), ('Pending', 'Pending')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='typeofproject',
            field=models.CharField(choices=[('Interior Fit-out Works', 'Interior Fit-outWorks'), ('Industrial Cement Flooring Finish', 'Industrial Cement Flooring Finish'), ('General Construction', 'General Construction'), ('Concrete Countertops', 'Concrete Countertops'), ('Self-Leveling Floor Applcation', 'Self-Leveling Floor Applcation')], max_length=255, null=True, verbose_name='Project Type'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Pending', 'Pending')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='status',
            field=models.CharField(choices=[('To be Delivered', 'To be Delivered'), ('Closed', 'Closed'), ('Pending', 'Pending')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='requisitiondetails',
            name='status2',
            field=models.CharField(blank=True, choices=[('Complete', 'Complete'), ('Incomplete', 'Incomplete'), ('Not Recieved', 'Not Recieved')], max_length=255, null=True, verbose_name='Action'),
        ),
    ]