from trainings_translations.models import TrainingTranslation
from django import forms

class FormTrainingTranslation(forms.ModelForm):
  
  class Meta:
    model = TrainingTranslation
    exclude = ('training', 'version', )

  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['title'].widget.attrs['autofocus'] = True

  def disable(self):
    self.fields['title'].widget.attrs['readonly'] = True