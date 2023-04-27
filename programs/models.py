from trainings.models import Training
from django.db import models

class Program(models.Model):
  training = models.ForeignKey(Training, on_delete=models.CASCADE)
  title = models.CharField(max_length=32)
  description = models.TextField(blank=True, null=True)
  must_know = models.TextField(blank=True, null=True)
  requirements = models.TextField(blank=True, null=True)