# Generated by Django 4.2.1 on 2023-05-22 13:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Shepherd', '0006_rename_reward_points_dailylogin_points'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailylogin',
            name='login_date',
        ),
        migrations.AddField(
            model_name='dailylogin',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='points',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='dailylogin',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
