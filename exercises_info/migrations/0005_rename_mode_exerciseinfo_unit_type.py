# Generated by Django 3.2.6 on 2023-06-26 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises_info', '0004_exerciseinfo_mode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exerciseinfo',
            old_name='mode',
            new_name='unit_type',
        ),
    ]
