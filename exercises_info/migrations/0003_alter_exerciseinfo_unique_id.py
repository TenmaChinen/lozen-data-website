# Generated by Django 3.2.6 on 2023-06-14 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises_info', '0002_alter_exerciseinfo_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exerciseinfo',
            name='unique_id',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]