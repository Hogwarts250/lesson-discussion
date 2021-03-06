# Generated by Django 3.0.9 on 2020-08-06 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repeat', models.CharField(choices=[('never', 'Never'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], default='never', max_length=7)),
                ('length', models.DurationField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('date', models.DateField()),
            ],
        ),
    ]
