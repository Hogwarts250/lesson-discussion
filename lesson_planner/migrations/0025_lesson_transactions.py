# Generated by Django 3.1 on 2020-08-17 02:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_transaction_note'),
        ('lesson_planner', '0024_remove_lesson_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='transactions',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.transaction'),
        ),
    ]
