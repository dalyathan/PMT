# Generated by Django 3.1 on 2021-08-18 11:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projmangtool', '0017_task_assigned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='dev',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
