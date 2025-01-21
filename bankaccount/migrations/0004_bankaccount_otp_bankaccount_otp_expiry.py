# Generated by Django 5.0.7 on 2024-07-28 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankaccount', '0003_bankaccount_daily_remaining_limit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='otp_expiry',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
