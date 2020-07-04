# Generated by Django 3.0.7 on 2020-07-04 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0018_auto_20200704_2130'),
    ]

    operations = [
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
            model_name='projectprogressdetails',
            name='level',
            field=models.IntegerField(choices=[(1, 'low'), (3, 'medium'), (5, 'high')], default=1, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='status',
            field=models.CharField(choices=[('Done', 'Done'), ('Pending', 'Pending'), ('On-going', 'On-going')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='status',
            field=models.CharField(blank=True, choices=[('Completed', 'Completed'), ('Completed (Overdue)', 'Completed (Overdue)'), ('Pending', 'Pending'), ('On-going', 'On-going')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('Rejected', 'Rejected'), ('Pending', 'Pending'), ('Accepted', 'Accepted')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='status',
            field=models.CharField(choices=[('Closed', 'Closed'), ('Pending', 'Pending'), ('To be Delivered', 'To be Delivered')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='requisitiondelivery',
            name='status2',
            field=models.CharField(blank=True, choices=[('Complete', 'Complete'), ('Incomplete', 'Incomplete'), ('Not Received', 'Not Received')], max_length=255, null=True, verbose_name='Action'),
        ),
    ]
