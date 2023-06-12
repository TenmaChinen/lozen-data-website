from exercises_info.models import ExerciseInfo
from languages.models import Language
from django.db import models

class ExerciseInfoTranslation(models.Model):
  exercise_info = models.ForeignKey(ExerciseInfo, on_delete=models.CASCADE)
  language = models.ForeignKey(Language, on_delete=models.CASCADE, blank=False, null=False)
  title = models.CharField(max_length=32, blank=True, null=True)
  description = models.TextField(blank=True, default='')
  version = models.PositiveSmallIntegerField()
  
  class Meta:
    unique_together = ('exercise_info','language',)