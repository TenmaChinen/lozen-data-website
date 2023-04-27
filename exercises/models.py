from programs.models import Program
from weeks_days.models import Day
from django.db import models

class Exercise(models.Model):
  # TODO : This should be Exercise Info ID 
  #  exercise names will be part of the exercise info section as selector )
  title = models.CharField(max_length=32)
  day = models.ForeignKey(Day, on_delete=models.CASCADE)
  idx = models.PositiveSmallIntegerField(blank=False, null=False)
  rounds = models.PositiveSmallIntegerField(blank=True, null=True)
  reps = models.PositiveSmallIntegerField(blank=True, null=True)
  percent = models.PositiveSmallIntegerField(blank=True, null=True)
  power = models.PositiveSmallIntegerField(blank=True, null=True)
  rir = models.PositiveSmallIntegerField(blank=True, null=True)
  rest = models.PositiveSmallIntegerField(blank=True, default=0)

  def rest_minutes(self):
    return self.rest // 60
  
  def rest_seconds(self):
    return self.rest % 60