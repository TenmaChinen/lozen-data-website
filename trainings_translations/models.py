from languages.models import Language
from trainings.models import Training
from django.db import models

class TrainingTranslation(models.Model):
  training = models.ForeignKey(Training, on_delete=models.CASCADE, blank=False, null=False)
  language = models.ForeignKey(Language, on_delete=models.CASCADE, blank=False, null=False)
  title = models.CharField(max_length=32, blank=True, null=True)
  version = models.PositiveSmallIntegerField()
  
  class Meta:
    unique_together = ('training', 'language',)