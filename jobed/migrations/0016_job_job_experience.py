# Generated by Django 5.1.2 on 2024-10-21 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobed', '0015_job_job_description_job_job_requirement'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_experience',
            field=models.TextField(blank=True, null=True),
        ),
    ]