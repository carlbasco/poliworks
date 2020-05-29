# Generated by Django 3.0.4 on 2020-05-29 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='construction.City', verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Done', 'Done'), ('On-going', 'On-going')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='construction.City', verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='projectsite',
            field=models.CharField(max_length=255, null=True, verbose_name='Project Name'),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('On-going', 'On-going')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='typeofproject',
            field=models.CharField(choices=[('Industrial Cement Flooring Finish', 'Industrial Cement Flooring Finish'), ('Self-Leveling Floor Applcation', 'Self-Leveling Floor Applcation'), ('Concrete Countertops', 'Concrete Countertops'), ('Interior Fit-out Works', 'Interior Fit-outWorks'), ('General Construction', 'General Construction')], max_length=255, null=True, verbose_name='Project Type'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Rejected', 'Rejected'), ('Accepted', 'Accepted')], default='Pending', max_length=255, verbose_name='Status'),
        ),
    ]
