# Generated by Django 5.0.4 on 2024-04-27 17:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_delete_booking'),
        ('bookings', '0010_booking_insurance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='car',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.car'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='insurance',
            field=models.CharField(default='normal or not', max_length=50),
        ),
    ]
