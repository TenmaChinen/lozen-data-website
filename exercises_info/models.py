from django.db import models

class ExerciseInfo(models.Model):
  MODE_CHOICES = [(0,'Reps'), (1,'Time')]

  # TODO : Document the use of NON automatic primary key.
  id = models.PositiveIntegerField(primary_key=True)
  unique_id = models.CharField(max_length=32, unique=True, blank=False, null=False)
  unit_type = models.SmallIntegerField(choices=MODE_CHOICES, default=False)
  # image = models.ImageField()
  version = models.PositiveSmallIntegerField(blank=False, null=False)

  # TODO : Change this to return the file_name or unique_id
  def __str__(self):
    return self.unique_id

  @classmethod
  def get_new_id(cls):
    if cls.objects.exists():
      return cls.objects.latest('id').id + 1
    else:
      return 1