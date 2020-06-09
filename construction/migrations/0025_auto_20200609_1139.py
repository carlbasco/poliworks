# Generated by Django 3.0.4 on 2020-06-09 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0024_auto_20200609_1024'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectinventory',
            options={'verbose_name': 'ProjectSite Inventory', 'verbose_name_plural': 'ProjectSite Inventory'},
        ),
        migrations.AlterField(
            model_name='personnel',
            name='sex',
            field=models.CharField(choices=[('Female', 'Female'), ('Male', 'Male')], max_length=10, verbose_name='Sex'),
        ),
        migrations.AlterField(
            model_name='projectinventorydetails',
            name='quantity',
            field=models.IntegerField(blank=True, null=True, verbose_name='Quantity'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='level',
            field=models.IntegerField(choices=[(5, 'high'), (3, 'medium'), (1, 'low')], default=1, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='status',
            field=models.CharField(blank=True, choices=[('Completed', 'Completed'), ('On-going', 'On-going'), ('Pending', 'Pending')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='typeofproject',
            field=models.CharField(choices=[('General Construction', 'General Construction'), ('Self-Leveling Floor Applcation', 'Self-Leveling Floor Applcation'), ('Concrete Countertops', 'Concrete Countertops'), ('Interior Fit-out Works', 'Interior Fit-outWorks'), ('Industrial Cement Flooring Finish', 'Industrial Cement Flooring Finish')], max_length=255, null=True, verbose_name='Project Type'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('Rejected', 'Rejected'), ('Accepted', 'Accepted'), ('Pending', 'Pending')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='status',
            field=models.CharField(choices=[('To be Delivered', 'To be Delivered'), ('Complied', 'Complied'), ('Completed', 'Completed'), ('Pending', 'Pending')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='requisitiondetails',
            name='status2',
            field=models.CharField(blank=True, choices=[('Incomplete', 'Incomplete'), ('Not Recieved', 'Not Recieved'), ('Complete', 'Complete')], max_length=255, null=True, verbose_name='Action'),
        ),
    ]
