from programs.models import Program
from django.db import models

T_WEEKS = ( (week,week) for week in range(1,20))
T_DAYS = ( (week,week) for week in range(1,8))

class Week(models.Model):
  program = models.ForeignKey(Program, on_delete=models.CASCADE)
  week = models.PositiveSmallIntegerField(choices=T_WEEKS)

class Day(models.Model):
  week = models.ForeignKey(Week, on_delete=models.CASCADE)
  day = models.PositiveSmallIntegerField(choices=T_DAYS)