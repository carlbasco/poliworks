# Generated by Django 3.0.8 on 2020-07-20 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0013_auto_20200720_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='requisition',
            name='amount',
            field=models.FloatField(default=0, verbose_name='Total Amount'),
        ),
        migrations.AlterField(
            model_name='jobordertask',
            name='status',
            field=models.CharField(choices=[('Done', 'Done'), ('Pending', 'Pending'), ('On-going', 'On-going')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('Currently Assigned', 'Currently Assigned')], default='Available', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('On-going', 'On-going'), ('Completed', 'Completed'), ('Completed (Overdue)', 'Completed (Overdue)')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='level',
            field=models.IntegerField(choices=[(5, 'high'), (3, 'medium'), (1, 'low')], default=1, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='status',
            field=models.CharField(choices=[('Done', 'Done'), ('Pending', 'Pending'), ('On-going', 'On-going')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='status',
            field=models.CharField(choices=[('To be Delivered', 'To be Delivered'), ('Pending', 'Pending'), ('Closed', 'Closed')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='requisitiondelivery',
            name='status2',
            field=models.CharField(blank=True, choices=[('Incomplete', 'Incomplete'), ('Not Received', 'Not Received'), ('Complete', 'Complete')], max_length=255, null=True, verbose_name='Action'),
        ),
    ]