from exercises_info_translations.models import ExerciseInfoTranslation
from django import forms

class FormExerciseInfoTranslation(forms.ModelForm):
  
  class Meta:
    model = ExerciseInfoTranslation
    exclude = ('exercise_info', 'version', )


  def disable(self):
    self.fields['title'].widget.attrs['disabled'] = True
    self.fields['description'].widget.attrs['disabled'] = True