# Generated by Django 3.0.4 on 2020-06-05 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0006_auto_20200604_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobordertask',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Done', 'Done')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='level',
            field=models.IntegerField(choices=[(3, 'medium'), (1, 'low'), (5, 'high')], default=1, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Done', 'Done'), ('On-going', 'On-going')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='status',
            field=models.CharField(blank=True, choices=[('Completed', 'Completed'), ('Pending', 'Pending'), ('On-going', 'On-going')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='typeofproject',
            field=models.CharField(choices=[('Self-Leveling Floor Applcation', 'Self-Leveling Floor Applcation'), ('Industrial Cement Flooring Finish', 'Industrial Cement Flooring Finish'), ('Interior Fit-out Works', 'Interior Fit-outWorks'), ('General Construction', 'General Construction'), ('Concrete Countertops', 'Concrete Countertops')], max_length=255, null=True, verbose_name='Project Type'),
        ),
    ]