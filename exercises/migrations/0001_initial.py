# Generated by Django 3.2.6 on 2023-05-04 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exercises_info', '0001_initial'),
        ('programs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.PositiveSmallIntegerField(choices=[(1, 'Week 1'), (2, 'Week 2'), (3, 'Week 3'), (4, 'Week 4'), (5, 'Week 5'), (6, 'Week 6'), (7, 'Week 7'), (8, 'Week 8'), (9, 'Week 9'), (10, 'Week 10'), (11, 'Week 11'), (12, 'Week 12'), (13, 'Week 13'), (14, 'Week 14'), (15, 'Week 15'), (16, 'Week 16'), (17, 'Week 17'), (18, 'Week 18'), (19, 'Week 19'), (20, 'Week 20')], default=1)),
                ('day', models.PositiveSmallIntegerField(choices=[(1, 'Day 1'), (2, 'Day 2'), (3, 'Day 3'), (4, 'Day 4'), (5, 'Day 5'), (6, 'Day 6'), (7, 'Day 7')], default=1)),
                ('index', models.PositiveSmallIntegerField()),
                ('rounds', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('reps', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('percent', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('power', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('rir', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('rest', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('exercise_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercises_info.exerciseinfo')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='programs.program')),
            ],
            options={
                'ordering': ['week', 'day', 'index'],
            },
        ),
    ]
