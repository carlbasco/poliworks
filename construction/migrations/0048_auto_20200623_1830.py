# Generated by Django 3.0.7 on 2020-06-23 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0047_auto_20200623_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='personnel',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='personnel',
            name='date2',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='jobordertask',
            name='status',
            field=models.CharField(choices=[('Done', 'Done'), ('Pending', 'Pending'), ('On-going', 'On-going')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='sex',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, verbose_name='Sex'),
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
            field=models.CharField(blank=True, choices=[('Completed', 'Completed'), ('Pending', 'Pending'), ('On-going', 'On-going')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='typeofproject',
            field=models.CharField(choices=[('Industrial Cement Flooring Finish', 'Industrial Cement Flooring Finish'), ('General Construction', 'General Construction'), ('Interior Fit-out Works', 'Interior Fit-outWorks'), ('Self-Leveling Floor Applcation', 'Self-Leveling Floor Applcation'), ('Concrete Countertops', 'Concrete Countertops')], max_length=255, null=True, verbose_name='Project Type'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='status',
            field=models.CharField(choices=[('To be Delivered', 'To be Delivered'), ('Pending', 'Pending'), ('Closed', 'Closed')], default='Pending', max_length=255),
        ),
    ]