from django.db import models

class ExerciseInfo(models.Model):
  # TODO : Document the use of NON automatic primary key.
  id = models.PositiveIntegerField(primary_key=True)
  title = models.CharField(max_length=32)
  description = models.TextField(blank=True, default='')

  def __str__(self):
    return self.title

  @classmethod
  def get_new_id(cls):
    if cls.objects.exists():
      return cls.objects.latest('id').id + 1
    else:
      return 1