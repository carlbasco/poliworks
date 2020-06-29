# Generated by Django 3.0.7 on 2020-06-29 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0058_auto_20200629_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personnel',
            name='personnel_type',
            field=models.CharField(choices=[('Company Worker', 'Company Worker'), ('Subcontractor', 'Subcontractor')], max_length=255, verbose_name='Type of Personnel'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='status',
            field=models.CharField(choices=[('Currently Assigned', 'Currently Assigned'), ('Available', 'Available')], default='Available', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='level',
            field=models.IntegerField(choices=[(1, 'low'), (3, 'medium'), (5, 'high')], default=1, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='status',
            field=models.CharField(blank=True, choices=[('On-going', 'On-going'), ('Completed', 'Completed'), ('Completed (Overdue)', 'Completed (Overdue)'), ('Pending', 'Pending')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='typeofproject',
            field=models.CharField(choices=[('Concrete Countertops', 'Concrete Countertops'), ('Industrial Cement Flooring Finish', 'Industrial Cement Flooring Finish'), ('Interior Fit-out Works', 'Interior Fit-outWorks'), ('General Construction', 'General Construction'), ('Self-Leveling Floor Applcation', 'Self-Leveling Floor Applcation')], max_length=255, null=True, verbose_name='Project Type'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Pending', 'Pending')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='requisitiondetails',
            name='status2',
            field=models.CharField(blank=True, choices=[('Complete', 'Complete'), ('Incomplete', 'Incomplete'), ('Not Received', 'Not Received')], max_length=255, null=True, verbose_name='Action'),
        ),
    ]