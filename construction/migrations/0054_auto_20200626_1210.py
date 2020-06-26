# Generated by Django 3.0.7 on 2020-06-26 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0053_auto_20200626_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobordertask',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('On-going', 'On-going'), ('Done', 'Done')], default='Pending', max_length=255, verbose_name='Status'),
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
            model_name='projectprogressdetails',
            name='level',
            field=models.IntegerField(choices=[(5, 'high'), (1, 'low'), (3, 'medium')], default=1, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('On-going', 'On-going'), ('Done', 'Done')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='status',
            field=models.CharField(blank=True, choices=[('Completed (Overdue)', 'Completed (Overdue)'), ('Pending', 'Pending'), ('Completed', 'Completed'), ('On-going', 'On-going')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='typeofproject',
            field=models.CharField(choices=[('Industrial Cement Flooring Finish', 'Industrial Cement Flooring Finish'), ('Concrete Countertops', 'Concrete Countertops'), ('General Construction', 'General Construction'), ('Self-Leveling Floor Applcation', 'Self-Leveling Floor Applcation'), ('Interior Fit-out Works', 'Interior Fit-outWorks')], max_length=255, null=True, verbose_name='Project Type'),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('To be Delivered', 'To be Delivered'), ('Closed', 'Closed')], default='Pending', max_length=255),
        ),
    ]