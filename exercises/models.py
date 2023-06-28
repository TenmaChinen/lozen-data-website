from exercises_info.models import ExerciseInfo
from programs.models import Program
from django.db import models

L_WEEKS = [(week,f'Week {week}') for week in range(1,21)]
L_DAYS = [(day,f'Day {day}') for day in range(1,8)]

class Exercise(models.Model):
  exercise_info = models.ForeignKey(ExerciseInfo, on_delete=models.CASCADE)
  program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='exercises')
  week = models.PositiveSmallIntegerField(choices=L_WEEKS, blank=False,null=False, default=1)
  day = models.PositiveSmallIntegerField(choices=L_DAYS, blank=False,null=False, default=1)
  idx = models.PositiveSmallIntegerField(blank=False, null=False)
  sets = models.PositiveSmallIntegerField(blank=False, null=False)
  unit_value = models.PositiveSmallIntegerField(blank=True, null=True)
  percent = models.PositiveSmallIntegerField(blank=True, null=True)
  power = models.PositiveSmallIntegerField(blank=True, null=True)
  rir = models.PositiveSmallIntegerField(blank=True, null=True)
  rest = models.PositiveSmallIntegerField(blank=True, default=0)
  version = models.PositiveSmallIntegerField()

  def rest_minutes(self):
    return self.rest // 60
  
  def rest_seconds(self):
    return self.rest % 60
  
  def rest_format(self):
    return f'{self.rest_minutes():02d}:{self.rest_seconds():02d}'
  
  # TODO : Document "self._meta.fields" or "self._meta.get_fields()"
  @classmethod
  def get_fields(cls):
    return [ field.name for field in cls._meta.get_fields() ]
  
  @classmethod
  def get_csv_fields(cls):
    l_excluded = ['id', 'program', 'version']
    l_field_name = [ field.name for field in cls._meta.get_fields() if field.name not in l_excluded ]
    
    target_idx = l_field_name.index('exercise_info')
    l_field_name.pop(target_idx)
    l_field_name.insert(target_idx, 'exercise_info_id')
    return l_field_name
  

  class Meta:
    unique_together = ('program','week', 'day', 'idx', )
    ordering = ['week','day','idx']