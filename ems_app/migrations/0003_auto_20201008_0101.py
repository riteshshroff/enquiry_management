# Generated by Django 3.1.2 on 2020-10-07 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ems_app', '0002_auto_20201006_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquiry',
            name='enquiry_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='enquiry_subject',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]