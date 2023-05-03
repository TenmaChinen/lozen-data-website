from exercises_info.models import ExerciseInfo
from django import forms

class ExerciseInfoForm(forms.ModelForm):

  class Meta:
    model = ExerciseInfo
    fields = '__all__'
    