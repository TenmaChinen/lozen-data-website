# Generated by Django 3.2.6 on 2023-05-02 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises_info', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exerciseinfo',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
    ]
