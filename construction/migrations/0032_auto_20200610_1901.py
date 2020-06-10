# Generated by Django 3.0.7 on 2020-06-10 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0031_auto_20200610_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailysitephotos',
            name='reveal',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, null=True, verbose_name='Let the client view this?'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='personnel_type',
            field=models.CharField(choices=[('Subcontractor', 'Subcontractor'), ('Company Worker', 'Company Worker')], max_length=255, verbose_name='Type of Personnel'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='sex',
            field=models.CharField(choices=[('Female', 'Female'), ('Male', 'Male')], max_length=10, verbose_name='Sex'),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='status',
            field=models.CharField(blank=True, choices=[('On-going', 'On-going'), ('Completed', 'Completed'), ('Pending', 'Pending')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='typeofproject',
            field=models.CharField(choices=[('Self-Leveling Floor Applcation', 'Self-Leveling Floor Applcation'), ('General Construction', 'General Construction'), ('Concrete Countertops', 'Concrete Countertops'), ('Industrial Cement Flooring Finish', 'Industrial Cement Flooring Finish'), ('Interior Fit-out Works', 'Interior Fit-outWorks')], max_length=255, null=True, verbose_name='Project Type'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('To be Delivered', 'To be Delivered'), ('Closed', 'Closed')], default='Pending', max_length=255),
        ),
    ]