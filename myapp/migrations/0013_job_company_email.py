# Generated by Django 5.0.4 on 2024-04-29 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_rename_field_of_work_job_work_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='company_email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
    ]
