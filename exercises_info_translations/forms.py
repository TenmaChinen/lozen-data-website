from exercises_info_translations.models import ExerciseInfoTranslation
from django import forms

class FormExerciseInfoTranslation(forms.ModelForm):
  
  class Meta:
    model = ExerciseInfoTranslation
    exclude = ('exercise_info', 'version', )
