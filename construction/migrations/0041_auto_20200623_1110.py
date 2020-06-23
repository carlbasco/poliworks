# Generated by Django 3.0.7 on 2020-06-23 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0040_auto_20200623_0945'),
    ]

    operations = [
        migrations.RenameField(
            model_name='externalorder',
            old_name='or_image',
            new_name='image',
        ),
        migrations.AlterField(
            model_name='jobordertask',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Done', 'Done'), ('On-going', 'On-going')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='personnel_type',
            field=models.CharField(choices=[('Subcontractor', 'Subcontractor'), ('Company Worker', 'Company Worker')], max_length=255, verbose_name='Type of Personnel'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='sex',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, verbose_name='Sex'),
        ),
        migrations.AlterField(
            model_name='projectprogressdetails',
            name='level',
            field=models.IntegerField(choices=[(3, 'medium'), (5, 'high'), (1, 'low')], default=1, verbose_name='Level'),
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
            field=models.CharField(choices=[('Concrete Countertops', 'Concrete Countertops'), ('Interior Fit-out Works', 'Interior Fit-outWorks'), ('Industrial Cement Flooring Finish', 'Industrial Cement Flooring Finish'), ('General Construction', 'General Construction'), ('Self-Leveling Floor Applcation', 'Self-Leveling Floor Applcation')], max_length=255, null=True, verbose_name='Project Type'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='status',
            field=models.CharField(choices=[('To be Delivered', 'To be Delivered'), ('Pending', 'Pending'), ('Closed', 'Closed')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='requisitiondetails',
            name='status2',
            field=models.CharField(blank=True, choices=[('Complete', 'Complete'), ('Not Recieved', 'Not Recieved'), ('Incomplete', 'Incomplete')], max_length=255, null=True, verbose_name='Action'),
        ),
    ]
