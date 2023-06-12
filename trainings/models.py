from django.db import models

class Training(models.Model):
  unique_id = models.CharField(max_length=32, unique=True, blank=False, null=False)
  version = models.PositiveSmallIntegerField()