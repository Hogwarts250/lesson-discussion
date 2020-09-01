# Generated by Django 3.1 on 2020-08-29 21:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lesson_planner', '0037_auto_20200829_1058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='name',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='teacher',
        ),
        migrations.AddField(
            model_name='lesson',
            name='status',
            field=models.CharField(choices=[('request', 'Request'), ('create', 'Create'), ('denied', 'Denied')], default='create', max_length=7),
        ),
        migrations.AddField(
            model_name='series',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='series',
            name='students',
            field=models.ManyToManyField(related_name='series_students', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='series',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='series_teacher', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='students',
            field=models.ManyToManyField(related_name='lesson_students', to=settings.AUTH_USER_MODEL),
        ),
    ]