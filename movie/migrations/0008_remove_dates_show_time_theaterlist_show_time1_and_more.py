# Generated by Django 4.0.6 on 2022-07-22 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0007_show_time_remove_theaterlist_movies_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dates',
            name='show_time',
        ),
        migrations.AddField(
            model_name='theaterlist',
            name='show_time1',
            field=models.CharField(blank=True, choices=[('9:30AM', '9:30AM'), ('12:00PM', '12:00PM'), ('2:30PM', '2:30PM'), ('4:30PM', '4:30PM'), ('6:30PM', '6:30PM'), ('8:30PM', '8:30PM')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='theaterlist',
            name='show_time2',
            field=models.CharField(blank=True, choices=[('9:30AM', '9:30AM'), ('12:00PM', '12:00PM'), ('2:30PM', '2:30PM'), ('4:30PM', '4:30PM'), ('6:30PM', '6:30PM'), ('8:30PM', '8:30PM')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='theaterlist',
            name='show_time3',
            field=models.CharField(blank=True, choices=[('9:30AM', '9:30AM'), ('12:00PM', '12:00PM'), ('2:30PM', '2:30PM'), ('4:30PM', '4:30PM'), ('6:30PM', '6:30PM'), ('8:30PM', '8:30PM')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='theaterlist',
            name='show_time4',
            field=models.CharField(blank=True, choices=[('9:30AM', '9:30AM'), ('12:00PM', '12:00PM'), ('2:30PM', '2:30PM'), ('4:30PM', '4:30PM'), ('6:30PM', '6:30PM'), ('8:30PM', '8:30PM')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='theaterlist',
            name='show_time5',
            field=models.CharField(blank=True, choices=[('9:30AM', '9:30AM'), ('12:00PM', '12:00PM'), ('2:30PM', '2:30PM'), ('4:30PM', '4:30PM'), ('6:30PM', '6:30PM'), ('8:30PM', '8:30PM')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='theaterlist',
            name='show_time6',
            field=models.CharField(blank=True, choices=[('9:30AM', '9:30AM'), ('12:00PM', '12:00PM'), ('2:30PM', '2:30PM'), ('4:30PM', '4:30PM'), ('6:30PM', '6:30PM'), ('8:30PM', '8:30PM')], max_length=10, null=True),
        ),
        migrations.RemoveField(
            model_name='dates',
            name='theaterlist',
        ),
        migrations.AddField(
            model_name='dates',
            name='theaterlist',
            field=models.ManyToManyField(blank=True, to='movie.theaterlist'),
        ),
        migrations.DeleteModel(
            name='show_time',
        ),
    ]
