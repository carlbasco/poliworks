# Generated by Django 3.0.7 on 2020-06-26 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0054_auto_20200626_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobordertask',
            name='status',
            field=models.CharField(choices=[('Done', 'Done'), ('On-going', 'On-going'), ('Pending', 'Pending')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('Currently Assigned', 'Currently Assigned')], default='Available', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='projectinventory',
            name='projectsite',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='construction.ProjectSite', verbose_name='Project Site'),
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
            field=models.CharField(blank=True, choices=[('Completed', 'Completed'), ('Completed (Overdue)', 'Completed (Overdue)'), ('On-going', 'On-going'), ('Pending', 'Pending')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='typeofproject',
            field=models.CharField(choices=[('Concrete Countertops', 'Concrete Countertops'), ('General Construction', 'General Construction'), ('Industrial Cement Flooring Finish', 'Industrial Cement Flooring Finish'), ('Interior Fit-out Works', 'Interior Fit-outWorks'), ('Self-Leveling Floor Applcation', 'Self-Leveling Floor Applcation')], max_length=255, null=True, verbose_name='Project Type'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Pending', 'Pending')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='status',
            field=models.CharField(choices=[('Closed', 'Closed'), ('To be Delivered', 'To be Delivered'), ('Pending', 'Pending')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='requisitiondetails',
            name='status2',
            field=models.CharField(blank=True, choices=[('Incomplete', 'Incomplete'), ('Not Recieved', 'Not Recieved'), ('Complete', 'Complete')], max_length=255, null=True, verbose_name='Action'),
        ),
    ]