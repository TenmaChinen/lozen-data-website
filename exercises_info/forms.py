from exercises_info.models import ExerciseInfo
from django import forms

class FormExerciseInfo(forms.ModelForm):

  class Meta:
    model = ExerciseInfo
    exclude = ['version',]
    
  def disable(self):
    self.fields['unique_id'].widget.attrs['disabled'] = True