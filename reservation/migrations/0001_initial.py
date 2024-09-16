# Generated by Django 5.1.1 on 2024-09-16 06:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appointmenttime', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_fee', models.PositiveBigIntegerField()),
                ('payment_status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reservation', to='appointmenttime.appointment')),
            ],
        ),
    ]
