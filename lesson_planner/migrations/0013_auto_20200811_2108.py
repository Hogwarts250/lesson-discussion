# Generated by Django 3.1 on 2020-08-12 04:08

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('lesson_planner', '0012_auto_20200811_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]