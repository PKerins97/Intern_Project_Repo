# Generated by Django 4.2.1 on 2023-05-16 10:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Shepherd', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='points',
            name='id',
        ),
        migrations.AlterField(
            model_name='points',
            name='username',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
