# Generated by Django 4.0.6 on 2022-07-23 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0012_remove_booking_all_seat_booking_all_seat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='date',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='theater',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='time',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
