from trainings.models import Training
from django.db import models

class Program(models.Model):
  training = models.ForeignKey(Training, on_delete=models.CASCADE)
  unique_id = models.CharField(max_length=32, unique=True, blank=False, null=False)
  version = models.PositiveSmallIntegerField()