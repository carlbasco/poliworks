# Generated by Django 3.0.7 on 2020-06-26 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0052_auto_20200624_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobordertask',
            name='status',
            field=models.CharField(choices=[('On-going', 'On-going'), ('Pending', 'Pending'), ('Done', 'Done')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='status',
            field=models.CharField(choices=[('Currently Assigned', 'Currently Assigned'), ('Available', 'Available')], default='Available', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='status',
            field=models.CharField(choices=[('On-going', 'On-going'), ('Pending', 'Pending'), ('Done', 'Done')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='status',
            field=models.CharField(blank=True, choices=[('On-going', 'On-going'), ('Completed (Overdue)', 'Completed (Overdue)'), ('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='typeofproject',
            field=models.CharField(choices=[('Self-Leveling Floor Applcation', 'Self-Leveling Floor Applcation'), ('Industrial Cement Flooring Finish', 'Industrial Cement Flooring Finish'), ('Concrete Countertops', 'Concrete Countertops'), ('General Construction', 'General Construction'), ('Interior Fit-out Works', 'Interior Fit-outWorks')], max_length=255, null=True, verbose_name='Project Type'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Rejected', 'Rejected'), ('Accepted', 'Accepted')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Closed', 'Closed'), ('To be Delivered', 'To be Delivered')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='requisitiondetails',
            name='status2',
            field=models.CharField(blank=True, choices=[('Not Recieved', 'Not Recieved'), ('Complete', 'Complete'), ('Incomplete', 'Incomplete')], max_length=255, null=True, verbose_name='Action'),
        ),
    ]
