from django.db import models

T_STATES = ((False,"No released"), (True,"Released"))

class Tracking(models.Model):
  version = models.PositiveSmallIntegerField(primary_key=True)
  state = models.BooleanField(default=False, choices=T_STATES)
  release_date = models.DateField(blank=True, null=True)


  @classmethod
  def get_last_version_released(cls):
    if cls.objects.exists():
      queryset = cls.objects.filter(state=True)
      if queryset.exists():
        return queryset.latest('version').version
    return None

  @classmethod
  def get_last_version(cls):
    if cls.objects.exists():
      tracking = cls.objects.latest('version')
      if tracking.state == False:
        return tracking.version
    return -1
  
  @classmethod
  def is_last_version_released(cls):
    if cls.objects.exists():
      tracking = cls.objects.latest('version')
      return tracking.state == True
    return True
  
  @classmethod
  def is_add_track_allowed(cls):
    if cls.objects.exists():
      return cls.objects.latest('version').state == True
    return True
  
  
  