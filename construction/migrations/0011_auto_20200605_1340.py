# Generated by Django 3.0.4 on 2020-06-05 05:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0010_auto_20200605_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joborder',
            name='pic',
            field=models.ForeignKey(limit_choices_to={'groups__name': 'Person In-Charge'}, on_delete=django.db.models.deletion.CASCADE, related_name='joborder_pic', to=settings.AUTH_USER_MODEL, verbose_name='Project In-Charge'),
        ),
        migrations.AlterField(
            model_name='jobordertask',
            name='status',
            field=models.CharField(choices=[('Done', 'Done'), ('Pending', 'Pending')], default='Pending', max_length=255, verbose_name='Status'),
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
            field=models.IntegerField(choices=[(5, 'high'), (1, 'low'), (3, 'medium')], default=1, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='status',
            field=models.CharField(choices=[('Done', 'Done'), ('On-going', 'On-going'), ('Pending', 'Pending')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='status',
            field=models.CharField(blank=True, choices=[('Completed', 'Completed'), ('On-going', 'On-going'), ('Pending', 'Pending')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='typeofproject',
            field=models.CharField(choices=[('Concrete Countertops', 'Concrete Countertops'), ('Industrial Cement Flooring Finish', 'Industrial Cement Flooring Finish'), ('Interior Fit-out Works', 'Interior Fit-outWorks'), ('Self-Leveling Floor Applcation', 'Self-Leveling Floor Applcation'), ('General Construction', 'General Construction')], max_length=255, null=True, verbose_name='Project Type'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=255, verbose_name='Status'),
        ),
    ]
