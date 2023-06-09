from django.db import models

l_languages = 'English Spanish'.split(' ')


class Language(models.Model):
    LANGUAGE_CHOICES = [(idx, language)for idx, language in enumerate(l_languages, 1)]

    id = models.PositiveSmallIntegerField(primary_key=True, choices=LANGUAGE_CHOICES, default=1)
    abbreviation = models.CharField(null=False, blank=False, unique=True, max_length=5)

    def __str__(self):
        return l_languages[self.id-1]
