# Generated by Django 3.1 on 2020-08-16 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
