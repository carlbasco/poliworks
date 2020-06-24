# Generated by Django 3.0.7 on 2020-06-23 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0043_auto_20200623_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobordertask',
            name='status',
            field=models.CharField(choices=[('Done', 'Done'), ('Pending', 'Pending'), ('On-going', 'On-going')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='level',
            field=models.IntegerField(choices=[(1, 'low'), (5, 'high'), (3, 'medium')], default=1, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='status',
            field=models.CharField(choices=[('Done', 'Done'), ('Pending', 'Pending'), ('On-going', 'On-going')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='typeofproject',
            field=models.CharField(choices=[('Concrete Countertops', 'Concrete Countertops'), ('Interior Fit-out Works', 'Interior Fit-outWorks'), ('Self-Leveling Floor Applcation', 'Self-Leveling Floor Applcation'), ('Industrial Cement Flooring Finish', 'Industrial Cement Flooring Finish'), ('General Construction', 'General Construction')], max_length=255, null=True, verbose_name='Project Type'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('Rejected', 'Rejected'), ('Accepted', 'Accepted'), ('Pending', 'Pending')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='status',
            field=models.CharField(choices=[('Closed', 'Closed'), ('To be Delivered', 'To be Delivered'), ('Pending', 'Pending')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='requisitiondetails',
            name='status2',
            field=models.CharField(blank=True, choices=[('Complete', 'Complete'), ('Not Recieved', 'Not Recieved'), ('Incomplete', 'Incomplete')], max_length=255, null=True, verbose_name='Action'),
        ),
    ]