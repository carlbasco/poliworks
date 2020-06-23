# Generated by Django 3.0.7 on 2020-06-23 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0046_auto_20200623_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externalorderdetailsreport',
            name='articles',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='construction.ExternalProjectInventoryDetails'),
        ),
        migrations.AlterField(
            model_name='jobordertask',
            name='status',
            field=models.CharField(choices=[('Done', 'Done'), ('On-going', 'On-going'), ('Pending', 'Pending')], default='Pending', max_length=255, verbose_name='Status'),
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
            field=models.CharField(choices=[('General Construction', 'General Construction'), ('Self-Leveling Floor Applcation', 'Self-Leveling Floor Applcation'), ('Concrete Countertops', 'Concrete Countertops'), ('Industrial Cement Flooring Finish', 'Industrial Cement Flooring Finish'), ('Interior Fit-out Works', 'Interior Fit-outWorks')], max_length=255, null=True, verbose_name='Project Type'),
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
            field=models.CharField(blank=True, choices=[('Not Recieved', 'Not Recieved'), ('Incomplete', 'Incomplete'), ('Complete', 'Complete')], max_length=255, null=True, verbose_name='Action'),
        ),
    ]
