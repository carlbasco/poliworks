# Generated by Django 3.0.8 on 2020-07-20 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0014_auto_20200720_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Completed (Overdue)', 'Completed (Overdue)'), ('On-going', 'On-going')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='level',
            field=models.IntegerField(choices=[(3, 'medium'), (1, 'low'), (5, 'high')], default=1, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='requisition_no',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='requisition number'),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('To be Delivered', 'To be Delivered'), ('Closed', 'Closed')], default='Pending', max_length=255),
        ),
    ]
