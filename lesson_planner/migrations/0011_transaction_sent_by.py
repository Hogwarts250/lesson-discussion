# Generated by Django 3.1 on 2020-08-11 03:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lesson_planner', '0010_auto_20200810_0716'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='sent_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
