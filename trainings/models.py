from django.db import models

class Training(models.Model):
  title = models.CharField(max_length=32)

