# Generated by Django 5.1.2 on 2024-11-01 10:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobed', '0017_achievement_application_certification_education_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermodel',
            name='work_experience',
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='achievements',
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='certifications',
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='education',
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='projects',
        ),
        migrations.AddField(
            model_name='achievement',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_achievement', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='application',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_application', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='certification',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_certification', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='education',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_education', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projects',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_project', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='company',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_company', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='job',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_job', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyName', models.CharField(max_length=200)),
                ('work_type', models.CharField(choices=[('Internship', 'Internship'), ('Part-Time', 'Part-Time'), ('Full-Time', 'Full-Time')])),
                ('company_website', models.CharField(max_length=200)),
                ('location', models.CharField(choices=[('Bengaluru', 'Bengaluru'), ('Hyderabad', 'Hyderabad'), ('Pune', 'Pune'), ('Chennai', 'Chennai'), ('Mumbai', 'Mumbai'), ('Delhi', 'Delhi'), ('Gurugram', 'Gurugram'), ('Noida', 'Noida'), ('Kolkata', 'Kolkata'), ('Ahmedabad', 'Ahmedabad'), ('Coimbatore', 'Coimbatore'), ('Trivandrum', 'Trivandrum'), ('Kochi', 'Kochi'), ('Indore', 'Indore'), ('Jaipur', 'Jaipur'), ('Nagpur', 'Nagpur'), ('Mysuru', 'Mysuru'), ('Lucknow', 'Lucknow'), ('Surat', 'Surat'), ('Bhubaneswar', 'Bhubaneswar'), ('Visakhapatnam', 'Visakhapatnam'), ('Vadodara', 'Vadodara'), ('Patna', 'Patna'), ('Chandigarh', 'Chandigarh'), ('Bhopal', 'Bhopal'), ('Raipur', 'Raipur'), ('Vijayawada', 'Vijayawada'), ('Ranchi', 'Ranchi'), ('Jamshedpur', 'Jamshedpur'), ('Kanpur', 'Kanpur'), ('Agra', 'Agra'), ('Nashik', 'Nashik'), ('Gwalior', 'Gwalior'), ('Madurai', 'Madurai'), ('Rajkot', 'Rajkot'), ('Udaipur', 'Udaipur'), ('Aurangabad', 'Aurangabad'), ('Pondicherry', 'Pondicherry'), ('Gandhinagar', 'Gandhinagar'), ('Dehradun', 'Dehradun'), ('Shimla', 'Shimla'), ('Mangalore', 'Mangalore'), ('Tiruchirappalli', 'Tiruchirappalli'), ('Kozhikode', 'Kozhikode'), ('Vellore', 'Vellore'), ('Amritsar', 'Amritsar'), ('Faridabad', 'Faridabad'), ('Ghaziabad', 'Ghaziabad'), ('Meerut', 'Meerut'), ('Durgapur', 'Durgapur'), ('Siliguri', 'Siliguri'), ('Jodhpur', 'Jodhpur'), ('Aligarh', 'Aligarh'), ('Allahabad (Prayagraj)', 'Allahabad (Prayagraj)'), ('Varanasi', 'Varanasi'), ('Panaji', 'Panaji'), ('Guntur', 'Guntur'), ('Hubli', 'Hubli'), ('Belgaum', 'Belgaum'), ('Salem', 'Salem'), ('Thane', 'Thane'), ('Rourkela', 'Rourkela'), ('Jabalpur', 'Jabalpur'), ('Srinagar', 'Srinagar'), ('Ujjain', 'Ujjain'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Vapi', 'Vapi'), ('Anand', 'Anand'), ('Haldwani', 'Haldwani'), ('Moradabad', 'Moradabad'), ('Saharanpur', 'Saharanpur'), ('Jalgaon', 'Jalgaon'), ('Satara', 'Satara'), ('Tumkur', 'Tumkur'), ('Karimnagar', 'Karimnagar'), ('Bellary', 'Bellary'), ('Palakkad', 'Palakkad'), ('Erode', 'Erode'), ('Thanjavur', 'Thanjavur'), ('Tirunelveli', 'Tirunelveli')], max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('working', models.CharField(choices=[('Working Currently', 'Working Currently'), ('No', 'No')])),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_work', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='WorkExperince',
        ),
    ]
