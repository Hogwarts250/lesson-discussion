# Generated by Django 3.0.9 on 2020-08-08 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_room', '0004_auto_20200807_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
