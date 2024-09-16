# Generated by Django 5.1.1 on 2024-09-16 09:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
        ('user', '0003_alter_doctorprofile_experience_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='comment',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_comments', to='user.doctorprofile'),
        ),
    ]
