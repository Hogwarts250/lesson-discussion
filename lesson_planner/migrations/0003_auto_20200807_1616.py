# Generated by Django 3.0.9 on 2020-08-07 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson_planner', '0002_auto_20200806_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='label',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='length',
            field=models.DurationField(null=True),
        ),
    ]
