# Generated by Django 5.0.7 on 2024-07-28 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankaccount', '0005_bankaccount_otp_attempts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='otp_attempts',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
