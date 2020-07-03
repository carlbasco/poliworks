# Generated by Django 3.0.7 on 2020-07-03 16:37

import construction.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0014_auto_20200702_1417'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estimate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('phone', models.CharField(max_length=20, verbose_name='Contact Number')),
                ('email', models.CharField(max_length=255, verbose_name='Email')),
                ('call_time', models.CharField(max_length=255, verbose_name='Best time to call')),
                ('address', models.CharField(max_length=255, null=True)),
                ('lotarea', models.CharField(blank=True, help_text='Please indicate if square meter, square kilometer, square mile, hectare, acre', max_length=255, verbose_name='Lot Area')),
                ('budget', models.FloatField(max_length=255, verbose_name='Estimated Budget')),
                ('date_start', models.DateField(null=True, verbose_name='Estimated Date Start')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='construction.City', verbose_name='City')),
                ('province', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='construction.Province', verbose_name='Province')),
                ('typeofproject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='construction.ProjectType', verbose_name='Project Type')),
            ],
        ),
        migrations.CreateModel(
            name='EstimateImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to=construction.models.estimate_upload_path, verbose_name='Image/Design/Reference')),
                ('estimate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='construction.Estimate')),
            ],
        ),
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('phone', models.CharField(max_length=20, verbose_name='Contact Number')),
                ('email', models.CharField(max_length=255, verbose_name='Email')),
                ('message', models.CharField(max_length=255, verbose_name='Message')),
                ('datetime', models.DateField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name='RequisitionStatus',
        ),
        migrations.AlterField(
            model_name='jobordertask',
            name='status',
            field=models.CharField(choices=[('Done', 'Done'), ('On-going', 'On-going'), ('Pending', 'Pending')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='level',
            field=models.IntegerField(choices=[(1, 'low'), (5, 'high'), (3, 'medium')], default=1, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='status',
            field=models.CharField(choices=[('Done', 'Done'), ('On-going', 'On-going'), ('Pending', 'Pending')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='status',
            field=models.CharField(blank=True, choices=[('Completed (Overdue)', 'Completed (Overdue)'), ('Completed', 'Completed'), ('On-going', 'On-going'), ('Pending', 'Pending')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('Rejected', 'Rejected'), ('Accepted', 'Accepted'), ('Pending', 'Pending')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='status',
            field=models.CharField(choices=[('To be Delivered', 'To be Delivered'), ('Closed', 'Closed'), ('Pending', 'Pending')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='requisitiondelivery',
            name='status2',
            field=models.CharField(blank=True, choices=[('Complete', 'Complete'), ('Not Received', 'Not Received'), ('Incomplete', 'Incomplete')], max_length=255, null=True, verbose_name='Action'),
        ),
    ]
