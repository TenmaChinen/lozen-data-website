from trainings.models import Training
from django import forms


class TrainingForm(forms.ModelForm):
  
  class Meta:
    model = Training
    exclude = ('version',)

  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['title'].widget.attrs['autofocus'] = True
  