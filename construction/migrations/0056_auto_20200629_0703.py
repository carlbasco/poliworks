# Generated by Django 3.0.7 on 2020-06-28 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0055_auto_20200626_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobordertask',
            name='status',
            field=models.CharField(choices=[('On-going', 'On-going'), ('Pending', 'Pending'), ('Done', 'Done')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='sex',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, verbose_name='Sex'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='status',
            field=models.CharField(choices=[('Currently Assigned', 'Currently Assigned'), ('Available', 'Available')], default='Available', max_length=255, verbose_name='Status'),
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
            model_name='projectsite',
            name='status',
            field=models.CharField(blank=True, choices=[('On-going', 'On-going'), ('Pending', 'Pending'), ('Completed', 'Completed'), ('Completed (Overdue)', 'Completed (Overdue)')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='typeofproject',
            field=models.CharField(choices=[('Concrete Countertops', 'Concrete Countertops'), ('Self-Leveling Floor Applcation', 'Self-Leveling Floor Applcation'), ('Industrial Cement Flooring Finish', 'Industrial Cement Flooring Finish'), ('General Construction', 'General Construction'), ('Interior Fit-out Works', 'Interior Fit-outWorks')], max_length=255, null=True, verbose_name='Project Type'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Closed', 'Closed'), ('To be Delivered', 'To be Delivered')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='requisitiondetails',
            name='status2',
            field=models.CharField(blank=True, choices=[('Complete', 'Complete'), ('Incomplete', 'Incomplete'), ('Not Recieved', 'Not Recieved')], max_length=255, null=True, verbose_name='Action'),
        ),
    ]