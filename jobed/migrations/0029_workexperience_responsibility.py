# Generated by Django 5.1.2 on 2024-11-19 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobed', '0028_alter_workexperience_company_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='workexperience',
            name='responsibility',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]
