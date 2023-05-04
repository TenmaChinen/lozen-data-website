from django.db import models

T_IDS = ((idx,idx) for idx in range(1,10))

l_languages = 'English Spanish'.split(' ')
T_LANGUAGES = ((idx,language) for idx, language in enumerate(l_languages,1))

class Language(models.Model):
  id = models.PositiveSmallIntegerField(primary_key=True,choices=T_LANGUAGES, default=1)

  def __str__(self):
    return l_languages[self.id-1]
  