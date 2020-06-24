# Generated by Django 3.0.7 on 2020-06-23 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0042_auto_20200623_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobordertask',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Done', 'Done'), ('On-going', 'On-going')], default='Pending', max_length=255, verbose_name='Status'),
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
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Done', 'Done'), ('On-going', 'On-going')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('On-going', 'On-going')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='typeofproject',
            field=models.CharField(choices=[('Interior Fit-out Works', 'Interior Fit-outWorks'), ('General Construction', 'General Construction'), ('Industrial Cement Flooring Finish', 'Industrial Cement Flooring Finish'), ('Self-Leveling Floor Applcation', 'Self-Leveling Floor Applcation'), ('Concrete Countertops', 'Concrete Countertops')], max_length=255, null=True, verbose_name='Project Type'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=255, verbose_name='Status'),
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
        migrations.CreateModel(
            name='ExternalProjectInventoryDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('articles', models.CharField(blank=True, max_length=255, null=True)),
                ('unit', models.CharField(blank=True, max_length=255, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='Quantity')),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='construction.ProjectInventory', verbose_name='Project Site Inventory')),
            ],
        ),
        migrations.CreateModel(
            name='ExternalProjectInventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_update', models.DateField(auto_now=True)),
                ('projectsite', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='construction.ProjectSite', verbose_name='Project Site')),
            ],
            options={
                'verbose_name': 'External ProjectSite Inventory',
                'verbose_name_plural': 'External ProjectSite Inventory',
            },
        ),
        migrations.AlterField(
            model_name='externalorderdetailsreport',
            name='articles',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='construction.ExternalProjectInventoryDetails'),
        ),
    ]