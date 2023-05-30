from languages.models import Language
from programs.models import Program
from django.db import models

class ProgramTranslation(models.Model):
  program = models.ForeignKey(Program, on_delete=models.CASCADE)
  language = models.ForeignKey(Language, on_delete=models.CASCADE, blank=False, null=False)
  title = models.CharField(max_length=32, blank=True, null=True)
  description = models.TextField(blank=True, null=True)
  must_know = models.TextField(blank=True, null=True)
  requirements = models.TextField(blank=True, null=True)
  version = models.PositiveSmallIntegerField()
  
  class Meta:
    unique_together = ('program','language',)